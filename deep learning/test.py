from PIL import Image  
from matplotlib.pylab import *  
import numpy as np  
import argparse  
import tensorflow as tf  
import time  
  
w = 128
h = 128

#这里是各种标志和交警手势的分类，可添加和更改
classes = ['forbid_run', 'forbid_straight',
           'forbid_turn_around', 'forbid_turn_right', 'forbid_whistle',
           'go straight', 'police_go_straight', 'police_slow_down',
           'police_stop', 'police_turn_left', 'police_turn_right',
           'speed_limit40', 'turn_left', 'turn_right']
  
def main(args):
    #测试文件位置，可更改
    fold_name = 'D:\\picbase\\test\\video_capture\\'
    model_dir = 'D:\\picbase\\test\\model\\model.ckpt'

    correct_number = 0
    # Restore model  
    saver = tf.train.import_meta_graph(model_dir+".meta")  
      
    with tf.Session() as sess:  
        saver.restore(sess, model_dir)  
        x = tf.get_default_graph().get_tensor_by_name("images:0")  
        keep_prob = tf.get_default_graph().get_tensor_by_name("keep_prob:0")  
        y = tf.get_default_graph().get_tensor_by_name("fc2/output:0")  
          

        for count in range(25,26):
            filename = fold_name + str(count) + '.jpg'
        # Read image
            time1 = time.time()
            pil_im = array(Image.open(filename).convert('L').resize((w,h)),dtype=float32)
            pil_im = pil_im/ 255.0
            pil_im = pil_im.reshape((1,w*h))
         

            prediction = sess.run(y, feed_dict={x:pil_im,keep_prob: 1.0})
            index = np.argmax(prediction)
            time2 = time.time()
            print("Now testing:", filename)
            #for pre in range(0, 19):
                #print(classes[pre], "|  probability:", prediction[0][pre]*100, " %" )
            print("The classes is: %s. (the probability is %g)" % (classes[index], prediction[0][index]))

            print("Using time %g s" % (time2-time1))
            if index == 13:
                correct_number += 1
        print("correct_number: ", correct_number)
def parse_arguments(argv):  
    parser = argparse.ArgumentParser()  
  
    parser.add_argument('--filename', type=str,  
                        help="The image name",default="D:\\picbase\\test\\capture\\turn_left\\image104.jpg")
    parser.add_argument('--model_dir', type=str,  
                        help="model file", default="D:\\picbase\\test\\model\\model.ckpt")
    return parser.parse_args(argv)  
  
if __name__=="__main__":  
    main(parse_arguments(sys.argv[1:]))  
