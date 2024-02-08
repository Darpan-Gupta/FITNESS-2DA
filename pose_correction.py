# Defining range for a perticular pose, after analysing the range from frequency graph of dataset

import numpy as np

import mediapipe as mp
mp_pose = mp.solutions.pose
import correct_posture_database

# import logging

# logging.basicConfig(level=logging.DEBUG)






landmark_positions = {'NOSE': 0, 'LEFT_EYE_INNER': 1, 'LEFT_EYE': 2, 'LEFT_EYE_OUTER': 3, 'RIGHT_EYE_INNER': 4, 'RIGHT_EYE': 5, 'RIGHT_EYE_OUTER': 6, 'LEFT_EAR': 7, 'RIGHT_EAR': 8, 'MOUTH_LEFT': 9, 'MOUTH_RIGHT': 10, 'LEFT_SHOULDER': 11, 'RIGHT_SHOULDER': 12, 'LEFT_ELBOW': 13, 'RIGHT_ELBOW': 14, 'LEFT_WRIST': 15, 'RIGHT_WRIST': 16, 'LEFT_PINKY': 17, 'RIGHT_PINKY': 18, 'LEFT_INDEX': 19, 'RIGHT_INDEX': 20, 'LEFT_THUMB': 21, 'RIGHT_THUMB': 22, 'LEFT_HIP': 23, 'RIGHT_HIP': 24, 'LEFT_KNEE': 25, 'RIGHT_KNEE': 26, 'LEFT_ANKLE': 27, 'RIGHT_ANKLE': 28, 'LEFT_HEEL': 29, 'RIGHT_HEEL': 30, 'LEFT_FOOT_INDEX': 31, 'RIGHT_FOOT_INDEX': 32}
# for i in mp_pose.PoseLandmark:
#     landmark_positions[str(i)[13:]] = i.value
# print('landmark_positions: ', landmark_positions)


joints_to_find_angle = {

    # keep the angle to find in the middle as the naming convention in this project is based on it
    
    'LEFT_SHOULDER' : ['LEFT_ELBOW', 'LEFT_SHOULDER', 'LEFT_HIP'],
    'RIGHT_SHOULDER' : ['RIGHT_ELBOW', 'RIGHT_SHOULDER', 'RIGHT_HIP'],
    'LEFT_ELBOW' : ['LEFT_WRIST', 'LEFT_ELBOW', 'LEFT_SHOULDER'],
    'RIGHT_ELBOW' : ['RIGHT_WRIST', 'RIGHT_ELBOW', 'RIGHT_SHOULDER'],
    'LEFT_HIP' : ['LEFT_SHOULDER', 'LEFT_HIP', 'LEFT_KNEE'],
    'RIGHT_HIP' : ['RIGHT_SHOULDER', 'RIGHT_HIP', 'RIGHT_KNEE'],
    'LEFT_KNEE' : ['LEFT_HIP', 'LEFT_KNEE', 'LEFT_ANKLE'],
    'RIGHT_KNEE' : ['RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_ANKLE']

}

def cal_angle(a,b,c):
    radians = np.arctan2(c.y-b.y, c.x-b.x) - np.arctan2(a.y-b.y, a.x-b.x)
    angle = np.abs(radians*180.0/np.pi)
    if angle>180.0:
        angle = 360-angle
    
    return angle


# we are considering 11 parameters for posture correctness
# correctness_checklist = [0]*11



def generate_correctness_checklist(correct_posture_range, current_feed_landmarks):
    
    # print('its working', correct_posture_range)




    correctness_checklist = [0]*11
    # logging.debug("logging its working", correctness_checklist)
    if 'neck_angle' in correct_posture_range:
        pass
        # cal_angle()
    for i, key in enumerate(joints_to_find_angle):
        joints = joints_to_find_angle[key]

        if joints[1] in correct_posture_range:
            if current_feed_landmarks[landmark_positions[joints[0]]].visibility > 0.5 and current_feed_landmarks[landmark_positions[joints[1]]].visibility > 0.5 and current_feed_landmarks[landmark_positions[joints[2]]].visibility > 0.5:

                angle = cal_angle(current_feed_landmarks[landmark_positions[joints[0]]],
                                current_feed_landmarks[landmark_positions[joints[1]]],
                                current_feed_landmarks[landmark_positions[joints[2]]])
            
                # print('angle', angle)

                if angle > correct_posture_range[joints[1]][0] and angle < correct_posture_range[joints[1]][1]:
                    correctness_checklist[i+1] = 1
                else:
                    correctness_checklist[i+1] = -1

    
   
                
    if 'wrist_distance' in correct_posture_range:
        pass
        # if current_feed_landmarks[landmark_positions['RIGHT_WRIST']].visibility > 0.5 and current_feed_landmarks[landmark_positions['LEFT_WRIST']].visibility > 0.5:
        
        #     if :
        #         correctness_checklist[9] = 1
        #     else:
        #         correctness_checklist[9] = -1

    if 'ankle_distance' in correct_posture_range:
        pass
        
        # if current_feed_landmarks[landmark_positions['RIGHT_ANKLE']].visibility > 0.5 and current_feed_landmarks[landmark_positions['LEFT_ANKLE']].visibility > 0.5:
        
        #     if :
        #         correctness_checklist[10] = 1
        #     else:
        #         correctness_checklist[10] = -1

    # print(correctness_checklist)
    # with open('temp.txt', 'a') as file:
    #     file.write(str(correctness_checklist))



    return(correctness_checklist)




        
# points to consider

# neck angle,
# shoulder angles,
# elbow angles,
# hip angles,
# knee angles,
# hand distance,
# foot distance,


remarks_list = [
    'Your neck is not correctly positioned',
    'Your left shoulder is not correctly postioned',
    'Your right shoulder is not correctly postioned',
    'Your left elbow is not correctly postioned',
    'Your right elbow is not correctly postioned',
    'Your left thigh is not correctly postioned',
    'Your right thigh is not correctly postioned',
    'Your left knee is not correctly postioned',
    'Your right knee is not correctly postioned',
    'Distance between hands is not correct',
    'Distance between ankles is not correct'
]

def generate_remarks(current_feed_landmarks, pose_name):

    # print(current_feed_landmarks)
    pose_name += "_correct_posture_range"
    
    correct_posture_range = getattr(correct_posture_database, pose_name)

    try:
        correctness_checklist = generate_correctness_checklist(correct_posture_range, current_feed_landmarks)
    except Exception as e:  # Catch all exceptions
        print("An unexpected error occurred:", e)

    
    feedback = []

    if correctness_checklist.count(0) > len(correctness_checklist)/2:
        feedback.append('You are not correctly visible in camera')
        return feedback
    
    for i in range(len(correctness_checklist)):
        if(correctness_checklist[i] == -1):
            feedback.append(remarks_list[i])

    if feedback == []:
        feedback.append('Correct Pose!!')

    return feedback

