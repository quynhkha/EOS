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

class CrystalImageObj:
    def __init__(self):
        pass

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
    def hist_extraction(cls, mask_id):
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
    def calc_confusion_matrix(cls, hist_objs, threshold):
        for hist_obj in hist_objs:
            for hist_obj_x in hist_objs:
                if hist_obj == hist_obj_x:
                    hist_obj.similarities.append({'similarity': "N/A", 'is_same_type': "N/A"})
                else:
                    hist_obj.similarities.append(cls.calc_hist_sim(hist_obj, hist_obj_x, threshold))
        return hist_objs

    @classmethod
    def calc_overall_sim(cls, hist_objs, mask_id, threshold):
        mask, image_cv, mask_cv = get_image_mask(mask_id)
        crystal_cv = ps_func.show_all_crystal(image_cv, mask_cv)
        hist_y_axis, hist_x_axis = ps_func.plot_histogram(image_cv, mask_cv)
        crystal_hist_obj = HistObj(hist_x_axis.tolist(), hist_y_axis.tolist(), None)
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
    def generate_sim_table(cls, mask_id, pair_thresh, overall_thresh):
        hist_objs = cls.hist_extraction(mask_id)
        hist_objs = cls.calc_confusion_matrix(hist_objs, pair_thresh)
        hist_objs = cls.calc_overall_sim(hist_objs, mask_id, overall_thresh)
        hist_objs = cls.count_num_pair(hist_objs)

        return hist_objs

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
