# TODO: remember hist_area
import cv2

from EOSWebApp.crystalManagement.models import Crystal
from EOSWebApp.imageProcessing.models import CrystalMask
from EOSWebApp.imageProcessing.processingFunc.crystal_extractor import ProcessingFunction
from EOSWebApp.utils import IMAGE_URL, TEMP_DIR, absolute_file_dir

ps_func = ProcessingFunction()
class HistObj:
    def __init__(self, x, y, crystal=None):
        self.x = x # a list
        self.y = y
        self.crystal = crystal
        self.similarities = []
        self.hist_area = 0
        self.num_pair = 0
        self.overall_sim = 0


class HistProcessing:
    @classmethod
    def calc_hist_sim(cls, h1, h2, threshold):
        total_common_area = 0

        # total common area
        for i in range(0, min(len(h1.x), len(h2.x))):
            common_area = min(h1.y[i], h2.y[i])
            total_common_area = total_common_area + common_area

        # min area (h1,h2)
        min_hist_area = min(cls.calc_hist_area(h1), cls.calc_hist_area(h2))

        similarity = (float(total_common_area) / float(min_hist_area))*100
        similarity = float("{0:.2f}".format(similarity)) # 2 decimal points
        # print("similarity", similarity)

        if similarity >= threshold:
            return {'similarity_percentage': similarity, 'is_same_type': True}
        else:
            return {'similarity_percentage': similarity, 'is_same_type': False}

    @classmethod
    def calc_hist_area(cls, h):
        area = 0
        for i in range(0, len(h.x)):
            area = area + h.y[i]
        return area

    @classmethod
    def prepare_hist_objs(cls, mask_id):
        # mask, image_cv, mask_cv = get_image_mask(mask_id)
        # file_infos = ps_func.save_crystals_to_file(mask.name, TEMP_DIR, image_cv, mask_cv)
        # hist_objs = []
        # for (file_dir, file_name) in file_infos:
        #     crystal_cv = cv2.imread(file_dir)
        #     hist_y_axis, hist_x_axis = ps_func.plot_histogram(crystal_cv)
        #     hist_obj = HistObj(hist_x_axis.tolist(), hist_y_axis.tolist(), mask_id,
        #                        file_name, file_dir)
        #     hist_obj.hist_area = cls.calc_hist_area(hist_obj)
        #     hist_objs.append(hist_obj)
        # return hist_objs
        mask_id = int(mask_id)
        mask = CrystalMask.objects.get(id=mask_id)
        crystals = Crystal.objects.filter(mask=mask)

        hist_objs = []
        for crystal in crystals:
            crystal_cv = cv2.imread(crystal.crystal.path)
            hist_y_axis, hist_x_axis = ps_func.plot_histogram(crystal_cv)
            hist_obj = HistObj(hist_x_axis.tolist(), hist_y_axis.tolist(), crystal)
            hist_objs.append(hist_obj)
        return hist_objs

    @classmethod
    def prepare_crystal_hist_obj(cls, mask_id):
        mask, image_cv, mask_cv = get_image_mask(mask_id)
        # crystal_cv = ps_func.show_all_crystal(image_cv, mask_cv)
        hist_y_axis, hist_x_axis = ps_func.plot_histogram(image_cv, mask_cv)
        crystal_hist_obj = HistObj(hist_x_axis.tolist(), hist_y_axis.tolist(), None)

        return crystal_hist_obj

    @classmethod
    def calc_confusion_matrix(cls, hist_objs, threshold):
        for hist_obj in hist_objs:
            for hist_obj_x in hist_objs:
                if hist_obj == hist_obj_x:
                    hist_obj.similarities.append({'similarity': "N/A", 'is_same_type': "N/A"})
                else:
                    hist_obj.similarities.append(cls.calc_hist_sim(hist_obj, hist_obj_x, threshold))
        return hist_objs

    @classmethod
    def calc_overall_sim(cls, hist_objs, crystal_hist_obj, mask_id, threshold):

        for hist_obj in hist_objs:
            hist_obj.overall_sim = cls.calc_hist_sim(hist_obj, crystal_hist_obj, threshold)

        return hist_objs

    @classmethod
    def count_num_pair(cls, hist_objs):
        for hist_obj in hist_objs:
            for similarity in hist_obj.similarities:
                if similarity['is_same_type'] == True:
                    hist_obj.num_pair = hist_obj.num_pair+1
        return hist_objs

    @classmethod
    def generate_result(cls, mask_id, pair_thresh, overall_thresh, trunc_min="None", trunc_max="None", comp_a="None", comp_b="None"):
        hist_objs = cls.prepare_hist_objs(mask_id)
        crystal_hist_obj = cls.prepare_crystal_hist_obj(mask_id)

        # truncate hist
        if trunc_min is not "None" and trunc_max is not "None":
            hist_objs, crystal_hist_obj = cls.update_trunc_hist(hist_objs, crystal_hist_obj, trunc_min, trunc_max)

        # composition
        if comp_a is not "None" and comp_b is not "None":
            hist_objs, crystal_hist_obj = cls.update_composition(hist_objs, crystal_hist_obj, comp_a, comp_b)

        overall_thresh = int(overall_thresh)
        pair_thresh= int(pair_thresh)
        hist_objs = cls.calc_confusion_matrix(hist_objs, pair_thresh)
        hist_objs = cls.calc_overall_sim(hist_objs, crystal_hist_obj, mask_id, overall_thresh)
        hist_objs = cls.count_num_pair(hist_objs)

        ref_section = cls.find_ref_section(hist_objs, overall_thresh)
        ideal_section = cls.find_idea_section(hist_objs)
        return hist_objs, ref_section, ideal_section

    @classmethod
    def find_ref_section(cls, hist_objs, overall_thresh):
        #sort descending by numpair
        desc_numpair_hist_objs = sorted(hist_objs, key=lambda x: x.num_pair, reverse=True)
        i = 0
        while i <len(desc_numpair_hist_objs):

            if int(desc_numpair_hist_objs[i].overall_sim['similarity_percentage'])< overall_thresh:
                i = i+1
            else:
                break
        if i < len(desc_numpair_hist_objs):
            ref_obj = desc_numpair_hist_objs[i]
            return ref_obj
        # no ref found
        else:
            return None

    @classmethod
    def find_idea_section(cls, hist_objs):
        #sort descending by overall sim
        desc_oversim_hist_objs = sorted(hist_objs, key=lambda x: x.overall_sim['similarity_percentage'], reverse=True)
        ideal_section = desc_oversim_hist_objs[0]
        return ideal_section

    @classmethod
    def update_trunc_hist(cls, hist_objs, crystal_hist_obj, trunc_min, trunc_max):
        for hist_obj in hist_objs:
            hist_obj = cls.calc_truncate_hist(hist_obj, trunc_min, trunc_max)

        crystal_hist_obj = cls.calc_truncate_hist(crystal_hist_obj, trunc_min, trunc_max)

        return hist_objs, crystal_hist_obj


    @classmethod
    def update_composition(cls, hist_objs, crystal_hist_obj, comp_a, comp_b):
        for hist_obj in hist_objs:
            hist_obj = cls.calc_composition(hist_obj, comp_a, comp_b)
        crystal_hist_obj = cls.calc_composition(crystal_hist_obj, comp_a, comp_b)

        return hist_objs, crystal_hist_obj

    @classmethod
    def calc_truncate_hist(cls, hist_obj, min_thresh, max_thresh):
        hist_range = int(max_thresh) - int(min_thresh)

        j = int(min_thresh)
        hist_x = []
        hist_y = []
        # only disp 100 bars
        if hist_range > 100:
            step = int(hist_range / 100) + 1  # floor
            for i in range(0, 100):
                y = 0
                x = i
                # aggregate hist in range together
                while (j < i * step and j <= int(max_thresh)):
                    y = y + hist_obj.y[j]
                    j = j + 1
                hist_x.append(x)
                hist_y.append(y)

        else:
            step = int(100 / hist_range)
            for i in range (0, 100):
                x = i
                y = 0
                if (i % step == 0):
                    if (j < int(max_thresh)):
                        y = hist_obj.y[j]
                        j = j + 1
                hist_x.append(x)
                hist_y.append(y)

        print(hist_x, hist_y)
        hist_obj.x = hist_x
        hist_obj.y = hist_y

        return hist_obj

    @classmethod
    def calc_composition(cls, hist_obj, a, b):
        a = float(a)
        b = int(b)

        # convert histogram by a
        data_length = int(len(hist_obj.x) * a) + 1
        hist_x = []
        hist_y = []
        if (a < 1):
            j = 0
            step = int(1 / a) + 1  # floor
            for i in range(0, data_length):
                x = i
                y = 0
                while (j < i * step and j < len(hist_obj.x)):
                    y = y + hist_obj.y[j]
                    j = j + 1
                hist_x.append(x)
                hist_y.append(y)

        else:
            step = int(a)
            j = 0
            for i in range(0, data_length):
                x = i
                y = 0
                if (i % step == 0):
                    if (j < len(hist_obj.x)):
                        y = hist_obj.y[j]
                        j = j + 1

                hist_x.append(x)
                hist_y.append(y)

        # move the hist based on b value
        new_hist_x = []
        new_hist_y = []
        for i in range(0, b):
            new_hist_x.append(0)
            new_hist_y.append(0)
        for i in range(0, len(hist_x)):
            new_hist_x.append(hist_x[i] + b)
            new_hist_y.append(hist_y[i])

        # update the hist_obj
        hist_obj.x = new_hist_x
        hist_obj.y = new_hist_y

        return hist_obj

def get_image_mask(mask_id):
    mask_id = int(mask_id)

    crystal_mask = CrystalMask.objects.get(pk=mask_id)
    mask_cv = cv2.imread(crystal_mask.mask.path)
    image = crystal_mask.image
    # image_file_dir = absolute_file_dir(image.filename, IMAGE_URL)
    # image_cv = cv2.imread(image_file_dir)
    image_cv = cv2.imread(image.image.path)
    # print("mask dir ", mask.mask_dir, "image dir ", image_file_dir)

    return crystal_mask, image_cv, mask_cv

# Generate table




