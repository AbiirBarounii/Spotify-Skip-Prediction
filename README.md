# Spotify Sequential Skip Prediction

Problem Statemnet: Predict if users will skip or listen to the music they're streamed

## Overview
Spotify is an online music streaming service with over 190 million active users interacting with a library of over 40 million tracks. A central challenge for Spotify is to recommend the right music to each user. While there is a large related body of work on recommender systems, there is very little work, or data, describing how users sequentially interact with the streamed content they are presented with. In particular within music, the question of if, and when, a user skips a track is an important implicit feedback signal.

Our challenge focuses on the task of session-based sequential skip prediction, i.e. predicting whether users will skip tracks, given their immediately preceding interactions in their listening session.

## DATASET
The public part of the dataset consists of roughly 130 million listening sessions with associated user interactions on the Spotify service. In addition to the public part of the dataset, approximately 30 million listening sessions are used for the challenge leaderboard. For these leaderboard sessions the participant is provided all the user interaction features for the first half of the session, but only the track id’s for the second half. In total, users interacted with almost 4 million tracks during these sessions, and the dataset includes acoustic features and metadata for all of these tracks.

If you use this dataset in an academic publication, please cite the following paper:

@inproceedings{brost2019music, title={The Music Streaming Sessions Dataset}, author={Brost, Brian and Mehrotra, Rishabh and Jehan, Tristan}, booktitle={Proceedings of the 2019 Web Conference}, year={2019}, organization={ACM} }

## CHALLENGE
The task is to predict whether individual tracks encountered in a listening session will be skipped by a particular user. In order to do this, complete information about the first half of a user’s listening session is provided, while the prediction is to be carried out on the second half. Participants have access to metadata, as well as acoustic descriptors, for all the tracks encountered in listening sessions.

The output of a prediction is a binary variable for each track in the second half of the session indicating if it was skipped or not, with a 1 indicating that the track skipped, and a 0 indicating that the track was not skipped. For this challenge we use the skip_2 field of the session logs as our ground truth.
