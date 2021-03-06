# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import sys
import cv2
import argparse
import random
import numpy as np
# import torch
# import torch.backends.cudnn as cudnn

# from utils.torch_utils import select_device
# from models.experimental import attempt_load
# from utils.general import check_img_size, non_max_suppression, scale_coords
# from utils.datasets import letterbox
# from utils.plots import plot_one_box

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self,parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.detectmode = '0'
        self.init_buttons()
        self.cap = cv2.VideoCapture()
        self.out = None

        # parser = argparse.ArgumentParser()
        # parser.add_argument('--weights', nargs='+', type=str,
        #                     default='weights/yolov5m.pt', help='model.pt path(s)')
        # # file/folder, 0 for webcam
        # parser.add_argument('--source', type=str,
        #                     default='data/images', help='source')
        # parser.add_argument('--img-size', type=int,
        #                     default=640, help='inference size (pixels)')
        # parser.add_argument('--conf-thres', type=float,
        #                     default=0.25, help='object confidence threshold')
        # parser.add_argument('--iou-thres', type=float,
        #                     default=0.45, help='IOU threshold for NMS')
        # parser.add_argument('--device', default='',
        #                     help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
        # parser.add_argument(
        #     '--view-img', action='store_true', help='display results')
        # parser.add_argument('--save-txt', action='store_true',
        #                     help='save results to *.txt')
        # parser.add_argument('--save-conf', action='store_true',
        #                     help='save confidences in --save-txt labels')
        # parser.add_argument('--nosave', action='store_true',
        #                     help='do not save images/videos')
        # parser.add_argument('--classes', nargs='+', type=int,
        #                     help='filter by class: --class 0, or --class 0 2 3')
        # parser.add_argument(
        #     '--agnostic-nms', action='store_true', help='class-agnostic NMS')
        # parser.add_argument('--augment', action='store_true',
        #                     help='augmented inference')
        # parser.add_argument('--update', action='store_true',
        #                     help='update all models')
        # parser.add_argument('--project', default='runs/detect',
        #                     help='save results to project/name')
        # parser.add_argument('--name', default='exp',
        #                     help='save results to project/name')
        # parser.add_argument('--exist-ok', action='store_true',
        #                     help='existing project/name ok, do not increment')
        # self.opt = parser.parse_args()

        # source, weights, view_img, save_txt, img_size = self.opt.source, self.opt.weights, self.opt.view_img, self.opt.save_txt, self.opt.img_size

        # self.device = select_device(self.opt.device)
        # self.half = self.device.type != 'cpu'  # half precision only supported on CUDA

        # cudnn.benchmark = True

        # self.model = attempt_load(
        #     weights, map_location=self.device)  # load FP32 model
        # stride = int(self.model.stride.max())  # model stride
        # self.imgsz = check_img_size(imgsz, s=stride)  # check img_size
        # if self.half:
        #     self.model.half()  # to FP16

        # # Get names and colors
        # self.names = self.model.module.names if hasattr(
        #     self.model, 'module') else self.model.names
        # self.colors = [[random.randint(0, 255)
        #                 for _ in range(3)] for _ in self.names]

    def init_buttons(self):
        self.pushButton.clicked.connect(self.button_img_open)
        self.radioButton.clicked.connect(self.changeState0)
        self.radioButton_2.clicked.connect(self.changeState1)
        self.pushButton_2.clicked.connect(self.button_img_detect)

    def changeState0(self):
        self.detectmode = '0'
    
    def changeState1(self):
        self.detectmode = '1'

    def button_img_open(self):
        img_list = []

        img_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open images", "", "*.jpg;;*.png;;All Files(*)")

        if not img_name:
            return
        
        img = cv2.imread(img_name)

        print(img_name)
        # self.result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        # self.result = cv2.resize(
        #     self.result, (640, 480), interpolation=cv2.INTER_AREA)
        # self.QtImg = QtGui.QImage(
        #     self.result.data, self.result.shape[1], self.result.shape[0], QtGui.QImage.Format_RGB32)
        self.label.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage(img_name)))
        self.label.setScaledContents(True)
        QtWidgets.QApplication.processEvents()

    def button_img_detect(self):
        # print(self.label.pixmap())
        # print(self.label.text())
        if not self.label.pixmap():
            QMessageBox.information(self,"Info","Choose a image first",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            return


        with torch.no_grad():

            img = letterbox(img, new_shape=self.opt.img_size)[0]
            # Convert
            img = img[:, :, ::-1].transpose(2, 0, 1)
            img = np.ascontiguousarray(img)
            img = torch.from_numpy(img).to(self.device)
            img = img.half() if self.half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)
            # Inference
            if self.detectmode == '0':
                pred = self.model(img, augment=self.opt.augment)[0]
            else:
                self.model = attempt_load(
                    self.opt.weights, map_location=self.device) 
                pred = self.model(img,augment=self.opt.augment)[0]
            # Apply NMS
            pred = non_max_suppression(pred, self.opt.conf_thres, self.opt.iou_thres, classes=self.opt.classes,
                                       agnostic=self.opt.agnostic_nms)
            print(pred)
            # Process detections
            for i, det in enumerate(pred):
                if det is not None and len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(
                        img.shape[2:], det[:, :4], showimg.shape).round()

                    for *xyxy, conf, cls in reversed(det):
                        label = '%s %.2f' % (self.names[int(cls)], conf)
                        annotator.box_label(xyxy,label,color=colors(c,True))
                        
                        # img_list.append(self.names[int(cls)])
                        # plot_one_box(xyxy, showimg, label=label,
                        #              color=self.colors[int(cls)], line_thickness=2)
            showimg = annotator.result()  

        cv2.imwrite('prediction.jpg', showimg)
        self.result = cv2.cvtColor(showimg, cv2.COLOR_BGR2BGRA)
        self.result = cv2.resize(
            self.result, (640, 480), interpolation=cv2.INTER_AREA)
        self.QtImg = QtGui.QImage(
            self.result.data, self.result.shape[1], self.result.shape[0], QtGui.QImage.Format_RGB32)
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.QtImg))


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(22, 20, 750, 500))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setMinimumSize(QtCore.QSize(200, 50))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.widget)
        self.radioButton.setMinimumSize(QtCore.QSize(180, 0))
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout.addWidget(self.radioButton_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.label = QtWidgets.QLabel(self.splitter)
        self.label.setMinimumSize(QtCore.QSize(500, 500))
        self.label.setText("")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 17))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Load Image"))
        self.radioButton.setText(_translate("MainWindow", "Best Performance"))
        self.radioButton_2.setText(_translate("MainWindow", "Light Weight"))
        self.pushButton_2.setText(_translate("MainWindow", "Detect"))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())