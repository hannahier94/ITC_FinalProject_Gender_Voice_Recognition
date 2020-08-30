# ITC_FinalProject_Gender_Voice_Recognition# ITC_FinalProject_Gender_Voice_Recognition

> Hebrew Subtitle Generator with Gender Consideration : By Serah Abensour, Yuval Herman, Hanna Hier, and Daniel Kagan

> This project aims to infuse gender recognition from audio clips with a Word2Word English -> Hebrew translator in order to generate more accurate subtitles given the various gender translations which exist in Hebrew. 



## Table of Contents

- [Overview](#Overview)
- [Clone](#Clone)
- [Requirements](#Requirements)
- [Usage](#Usage)
- [FAQ](#FAQ)

## Overview 

- The first model uses a Dense network to distinguish
- between male and female voices given preprocessed Englished
- audio clips (~92.5% accuracy). 
- A seperate network will be trained on male/female verbs 
- Next, we will use a Word2Word network to translate the phrases
- from English to Hebrew, with the additional input of the gender.
- Finally, we will connect the two pipelines using a speech2text
- between the audio gender detection and text translation. 
- An example of the end result should be as follows: 
- If a woman says "I am walking", it should output 
- אני הולכת , instead of the male equivalent: 
- אני הולך .

---
## Clone

Clone this repo to your local machine using `https://https://github.com/hannahier94/ITC_FinalProject_Gender_Voice_Recognition`

---

## Requirements

logger==1.4 \
pandas==1.0.3 \
pip~=20.1.1 \

---


## Badges
> Warning: The following badges are for display purposes only and may be considered fake news as they do not reflect actual information about this page. 

[![Fake Coverage](https://camo.githubusercontent.com/3eff610e3559385c77a9b6d87cbe1252cab79a4d/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f7665726167652d38302532352d79656c6c6f77677265656e)](https://travis-ci.org/badges/badgerbadgerbadger)  [![A Fake Rating](https://camo.githubusercontent.com/d5cd29c0e2930c3c4026ba87ff427e2e340f461b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f726174696e672d2545322539382538352545322539382538352545322539382538352545322539382538352545322539382538362d627269676874677265656e)](https://travis-ci.org/badges/badgerbadgerbadger)  [![A Fake 3rd Thing](https://camo.githubusercontent.com/b3fc74878a0d5fcca5a78b288aa4b489f65fd7eb/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f757074696d652d3130302532352d627269676874677265656e)](https://travis-ci.org/badges/badgerbadgerbadger)

---

## FAQ

- **What makes your voice translator better than other similar algorithms?**
    - Our algorithm takes the gender of the speaker into account when translating sentences, ultimately working to limit the gender bias in current translation APIs. Other APIs determine the male/female usage of verbs based on the context of the setence itself, which can lead to incorrect results. For example, if an algorithm has for seen from it's training data that most nurses are female. In this case, the likelihood of the sentence being spoken by a female would be higher so the output would imply this. Our algorithm does not depend on the bias of previous training data to come up with this result. We use additional information about the speaker (the voice gender recognition) to paint a more complete picture.
