import cv2 as cv
import numpy as np


# Блок поиска и отрисовки маркеров
dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)

#path = r"C:\Users\smoly\Downloads\singlemarkersoriginal.jpg"
path = r"C:\Users\smoly\Downloads\ThirdTry.png"
img = cv.imread(path)
cv.imshow('Input image', img)
cv.waitKey(3000)
cv.destroyWindow('Input image')

parameters = cv.aruco.DetectorParameters_create()
markerCorners, markerIds, rejectedCandidates = cv.aruco.detectMarkers(img, dictionary, parameters=parameters)
cv.aruco.drawDetectedMarkers(img, markerCorners, markerIds)
cv.imshow('Image with Aruco', img)
cv.waitKey(3000)
cv.destroyWindow('Image with Aruco')


# Блок калибровки камеры
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((9*6, 3), np.float32)
objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

objpoints = []
imgpoints = []

fname = r"C:\Users\smoly\Downloads\chessmate.jpg"
chess = cv.imread(fname)
gray = cv.cvtColor(chess, cv.COLOR_BGR2GRAY)

ret, corners = cv.findChessboardCorners(gray, (9, 6), None)

if ret == True:
    objpoints.append(objp)
    corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    imgpoints.append(corners2)
    cv.drawChessboardCorners(chess, (9, 6), corners2, ret)
    cv.imshow('Chessboard', chess)
    cv.waitKey(3000)
    cv.destroyWindow('Chessboard')

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)


# Блок отрисовки векторов
rvecs1, tvecs1, obj = cv.aruco.estimatePoseSingleMarkers(markerCorners, 0.05, mtx, dist)

for i in range(len(rvecs1)):
    auto_rvec = rvecs1[i]
    auto_tvec = tvecs1[i]
    cv.drawFrameAxes(img, mtx, dist, auto_rvec, auto_tvec, 0.05)

cv.imshow('Vectors', img)
cv.waitKey(0)
