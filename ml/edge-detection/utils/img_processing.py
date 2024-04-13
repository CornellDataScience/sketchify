import os

import cv2
import numpy as np
import torch
import kornia as kn

from skimage.metrics import mean_squared_error, peak_signal_noise_ratio
from sklearn.metrics import mean_absolute_error


def image_normalization(img, img_min=0, img_max=255,
                        epsilon=1e-12):
    """This is a typical image normalization function
    where the minimum and maximum of the image is needed
    source: https://en.wikipedia.org/wiki/Normalization_(image_processing)

    :param img: an image could be gray scale or color
    :param img_min:  for default is 0
    :param img_max: for default is 255

    :return: a normalized image, if max is 255 the dtype is uint8
    """

    img = np.float32(img)
    # whenever an inconsistent image
    img = (img - np.min(img)) * (img_max - img_min) / \
        ((np.max(img) - np.min(img)) + epsilon) + img_min
    return img

def count_parameters(model=None):
    if model is not None:
        return sum(p.numel() for p in model.parameters() if p.requires_grad)
    else:
        print("Error counting model parameters line 32 img_processing.py")
        raise NotImplementedError


def save_image_batch_to_disk(tensor, output_dir, file_names, img_shape=None, arg=None, is_inchannel=False):

    os.makedirs(output_dir, exist_ok=True)
    predict_all = arg.predict_all
    if not arg.is_testing:
        assert len(tensor.shape) == 4, tensor.shape
        img_height,img_width = img_shape[0].item(),img_shape[1].item()

        for tensor_image, file_name in zip(tensor, file_names):
            image_vis = kn.utils.tensor_to_image(
                torch.sigmoid(tensor_image))#[..., 0]
            image_vis = (255.0*(1.0 - image_vis)).astype(np.uint8)
            output_file_name = os.path.join(output_dir, file_name)
            # print('image vis size', image_vis.shape)
            image_vis =cv2.resize(image_vis, (img_width, img_height))
            assert cv2.imwrite(output_file_name, image_vis)
            assert cv2.imwrite('checkpoints/current_res/'+file_name, image_vis)
            # print(f"Image saved in {output_file_name}")
    else:
        if is_inchannel:

            tensor, tensor2 = tensor
            fuse_name = 'fusedCH'
            av_name='avgCH'
            is_2tensors=True
            edge_maps2 = []
            for i in tensor2:
                tmp = torch.sigmoid(i).cpu().detach().numpy()
                edge_maps2.append(tmp)
            tensor2 = np.array(edge_maps2)
        else:
            fuse_name = 'fused'
            # av_name = 'avg'
            tensor2=None
            tmp_img2 = None

        output_dir_f = os.path.join(output_dir, fuse_name)# normal execution
        # output_dir_f = output_dir# for DMRIR
        # output_dir_a = os.path.join(output_dir, av_name)
        os.makedirs(output_dir_f, exist_ok=True)
        # os.makedirs(output_dir_a, exist_ok=True)
        if predict_all:
            all_data_dir = os.path.join(output_dir, "all_edges")
            os.makedirs(all_data_dir, exist_ok=True)
            out1_dir = os.path.join(all_data_dir,"o1")
            out2_dir = os.path.join(all_data_dir,"o2")
            out3_dir = os.path.join(all_data_dir,"o3")#   TEED =output 3
            out4_dir = os.path.join(all_data_dir,"o4") # TEED = average
            out5_dir = os.path.join(all_data_dir,"o5")# fusion # TEED
            out6_dir = os.path.join(all_data_dir,"o6") # fusion
            os.makedirs(out1_dir, exist_ok=True)
            os.makedirs(out2_dir, exist_ok=True)
            os.makedirs(out3_dir, exist_ok=True)
            os.makedirs(out4_dir, exist_ok=True)
            os.makedirs(out5_dir, exist_ok=True)
            os.makedirs(out6_dir, exist_ok=True)

        # 255.0 * (1.0 - em_a)
        edge_maps = []
        for i in tensor:
            tmp = torch.sigmoid(i).cpu().detach().numpy()
            edge_maps.append(tmp)
        tensor = np.array(edge_maps)
        # print(f"tensor shape: {tensor.shape}")

        image_shape = [x.cpu().detach().numpy() for x in img_shape]
        # (H, W) -> (W, H)
        image_shape = [[y, x] for x, y in zip(image_shape[0], image_shape[1])]

        assert len(image_shape) == len(file_names)

        idx = 0
        for i_shape, file_name in zip(image_shape, file_names):
            tmp = tensor[:, idx, ...]
            tmp2 = tensor2[:, idx, ...] if tensor2 is not None else None
            # tmp = np.transpose(np.squeeze(tmp), [0, 1, 2])
            tmp = np.squeeze(tmp)
            tmp2 = np.squeeze(tmp2) if tensor2 is not None else None

            # Iterate our all 7 NN outputs for a particular image
            preds = []
            fuse_num = tmp.shape[0]-1
            for i in range(tmp.shape[0]):
                tmp_img = tmp[i]
                tmp_img = np.uint8(image_normalization(tmp_img))
                tmp_img = cv2.bitwise_not(tmp_img)
                # tmp_img[tmp_img < 0.0] = 0.0
                # tmp_img = 255.0 * (1.0 - tmp_img)
                if tmp2 is not None:
                    tmp_img2 = tmp2[i]
                    tmp_img2 = np.uint8(image_normalization(tmp_img2))
                    tmp_img2 = cv2.bitwise_not(tmp_img2)

                # Resize prediction to match input image size
                if not tmp_img.shape[1] == i_shape[0] or not tmp_img.shape[0] == i_shape[1]:
                    tmp_img = cv2.resize(tmp_img, (i_shape[0], i_shape[1]))
                    tmp_img2 = cv2.resize(tmp_img2, (i_shape[0], i_shape[1])) if tmp2 is not None else None


                if tmp2 is not None:
                    tmp_mask = np.logical_and(tmp_img>128,tmp_img2<128)
                    tmp_img= np.where(tmp_mask, tmp_img2, tmp_img)
                    preds.append(tmp_img)

                else:
                    preds.append(tmp_img)

                if i == fuse_num:
                    # print('fuse num',tmp.shape[0], fuse_num, i)
                    fuse = tmp_img
                    fuse = fuse.astype(np.uint8)
                    if tmp_img2 is not None:
                        fuse2 = tmp_img2
                        fuse2 = fuse2.astype(np.uint8)
                        # fuse = fuse-fuse2
                        fuse_mask=np.logical_and(fuse>128,fuse2<128)
                        fuse = np.where(fuse_mask,fuse2, fuse)

                        # print(fuse.shape, fuse_mask.shape)

            # Save predicted edge maps
            average = np.array(preds, dtype=np.float32)
            average = np.uint8(np.mean(average, axis=0))
            output_file_name_f = os.path.join(output_dir_f, file_name)
            # output_file_name_a = os.path.join(output_dir_a, file_name)
            cv2.imwrite(output_file_name_f, fuse)
            # cv2.imwrite(output_file_name_a, average)
            if predict_all:
                cv2.imwrite(os.path.join(out1_dir,file_name),preds[0])
                cv2.imwrite(os.path.join(out2_dir,file_name),preds[1])
                cv2.imwrite(os.path.join(out3_dir,file_name),preds[2])
                cv2.imwrite(os.path.join(out4_dir,file_name),average)
                cv2.imwrite(os.path.join(out5_dir,file_name),fuse)
                cv2.imwrite(os.path.join(out6_dir,file_name),fuse)

            idx += 1


def restore_rgb(config, I, restore_rgb=False):
    """
    :param config: [args.channel_swap, args.mean_pixel_value]
    :param I: and image or a set of images
    :return: an image or a set of images restored
    """

    if len(I) > 3 and not type(I) == np.ndarray:
        I = np.array(I)
        I = I[:, :, :, 0:3]
        n = I.shape[0]
        for i in range(n):
            x = I[i, ...]
            x = np.array(x, dtype=np.float32)
            x += config[1]
            if restore_rgb:
                x = x[:, :, config[0]]
            x = image_normalization(x)
            I[i, :, :, :] = x
    elif len(I.shape) == 3 and I.shape[-1] == 3:
        I = np.array(I, dtype=np.float32)
        I += config[1]
        if restore_rgb:
            I = I[:, :, config[0]]
        I = image_normalization(I)
    else:
        print("Sorry the input data size is out of our configuration")
    return I


def visualize_result(imgs_list, arg):
    """
    data 2 image in one matrix
    :param imgs_list: a list of prediction, gt and input data
    :param arg:
    :return: one image with the whole of imgs_list data
    """
    n_imgs = len(imgs_list)
    data_list = []
    for i in range(n_imgs):
        tmp = imgs_list[i]
        # print(tmp.shape)
        if tmp.shape[0] == 3:
            tmp = np.transpose(tmp, [1, 2, 0])
            tmp = restore_rgb([
                arg.channel_swap,
                arg.mean_train[:3]
            ], tmp)
            tmp = np.uint8(image_normalization(tmp))
        else:
            tmp = np.squeeze(tmp)
            if len(tmp.shape) == 2:
                tmp = np.uint8(image_normalization(tmp))
                tmp = cv2.bitwise_not(tmp)
                tmp = cv2.cvtColor(tmp, cv2.COLOR_GRAY2BGR)
            else:
                tmp = np.uint8(image_normalization(tmp))
        data_list.append(tmp)
        # print(i,tmp.shape)
    img = data_list[0]
    if n_imgs % 2 == 0:
        imgs = np.zeros((img.shape[0] * 2 + 10, img.shape[1]
                         * (n_imgs // 2) + ((n_imgs // 2 - 1) * 5), 3))
    else:
        imgs = np.zeros((img.shape[0] * 2 + 10, img.shape[1]
                         * ((1 + n_imgs) // 2) + ((n_imgs // 2) * 5), 3))
        n_imgs += 1

    k = 0
    imgs = np.uint8(imgs)
    i_step = img.shape[0] + 10
    j_step = img.shape[1] + 5
    for i in range(2):
        for j in range(n_imgs // 2):
            if k < len(data_list):
                imgs[i * i_step:i * i_step+img.shape[0],
                     j * j_step:j * j_step+img.shape[1],
                     :] = data_list[k]
                k += 1
            else:
                pass
    return imgs



if __name__ == '__main__':

    img_base_dir='tmp_edge'
    gt_base_dir='C:/Users/xavysp/dataset/BIPED/edges/edge_maps/test/rgbr'
    # gt_base_dir='C:/Users/xavysp/dataset/BRIND/test_edges'
    # gt_base_dir='C:/Users/xavysp/dataset/UDED/gt'
    vers = 'TEED model in BIPED'
    list_img = os.listdir(img_base_dir)
    list_gt = os.listdir(gt_base_dir)
    mse_list=[]
    psnr_list=[]
    mae_list=[]

    for img_name, gt_name in zip(list_img,list_gt):

        # print(img_name, '   ', gt_name)
        tmp_img = cv2.imread(os.path.join(img_base_dir,img_name),0)
        tmp_img = cv2.bitwise_not(tmp_img) # if the image's background
        # is white uncomment this line
        tmp_gt = cv2.imread(os.path.join(gt_base_dir,gt_name),0)
        # print(f"image {img_name} {tmp_img.shape}")
        # print(f"gt {gt_name} {tmp_gt.shape}")
        a = tmp_img.copy()
        tmp_img = image_normalization(tmp_img, img_max=1.)
        tmp_gt = image_normalization(tmp_gt, img_max=1.)
        psnr = peak_signal_noise_ratio(tmp_gt, tmp_img)
        mse = mean_squared_error(tmp_gt, tmp_img)
        mae = mean_absolute_error(tmp_gt, tmp_img)
        # a = cv2.bitwise_not(a) # save data
        # cv2.imwrite(os.path.join("tmp_res",img_name), a) # save data

        psnr_list.append(psnr)
        mse_list.append(mse)
        mae_list.append(mae)
        print(f"PSNR= {psnr} in {img_name}")

    av_psnr =np.array(psnr_list).mean()
    av_mse =np.array(mse_list).mean()
    av_mae =np.array(mae_list).mean()
    print(" MSE results: mean ", av_mse)
    print(" MAE results: mean ", av_mae)
    # print(mse_list)
    print(" PSNR results: mean", av_psnr)
    # print(psnr_list)
    print('version: ',vers)
