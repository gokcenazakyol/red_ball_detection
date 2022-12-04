import cv2 as cv
import pafy
import youtube_dl
import requests
import base64


def read_url(url):

    """
        This method helps to read the url from YouTube.
    """

    video = pafy.new(url)
    best = video.getbest(preftype="mp4")
    cap = cv.VideoCapture()
    cap.open(best.url)
    return cap


def draw_rectangle(contours, frame):

    """
        This method draws a box on detected object and
        labels it as 'RED_BALL'. Also returns the center
        points of detected red balls.
    """

    # creating a list to hold the detected objects' middle pixels
    points = []

    for cnt in contours:

        # calculating area to detect only ball, not every pixel with color red
        area = cv.contourArea(cnt)

        # if area is larger than 1000, we understand that it is red ball
        if area > 1000:
            x, y, w, h = cv.boundingRect(cnt)

            # to calculate middle points location (x + (x + w)) / 2 and (y + (y + h)) / 2
            cx = int((2 * x + w) / 2)
            cy = int((2 * y + h) / 2)

            points.append((cx, cy))

            # drawing rectangle on the detected object
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # labeling the detected object as 'RED_BALL'
            cv.putText(frame, "RED_BALL", (cx, cy - 45), fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=1,
                       color=(0, 250, 0), thickness=2)

    return points


def post_request(url, json):

    """
        This method sends post request to the given url.
    """

    r = requests.post(url, data=json)

    # Since r.text gives result as ok, I understood that everything is fine
    if r.status_code == requests.codes.ok:
        print(">>>Send POST REQUEST...")
        print(r.text)

def base64_converter(image):

    """
        Coverts image to base64.
    """

    with open(image, "rb") as img:
        encoded_img = base64.b64encode(img.read())
        return encoded_img


def show_error(points, counter, frame):

    """
        This function sends message to terminal if the number of
        red balls on the left side of the video is bigger than 3.
        Saves the image to the disk.
        Also, this method calls post_request().
    """

    # the specified url
    url = 'https://eldercare.unknownland.org/red_ball'

    if len(points) > 3:
        # sending message to terminal
        print("----------------------------------------")
        print("CAUTION......")
        print("Frame {frame_no}".format(frame_no=str(counter)))
        print("Number of red balls on the left side:", len(points))

        # saving the frame to the disk
        img = 'saved_frames/{counter}.jpeg'.format(counter=str(counter))
        cv.imwrite(img, frame)

        # sending post request
        encoded_img = base64_converter(img)
        json = {"red_ball": len(points), "picture": encoded_img}
        post_request(url, json)
