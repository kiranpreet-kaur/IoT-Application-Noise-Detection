

FROM python

RUN apt-get update
RUN pip install paho-mqtt

RUN apt-get install -y libasound2-dev libasound2-dev:armhf
#RUN apt-get install -y alsa-base alsa-utils
RUN apt install -y portaudio19-dev
RUN pip install pyaudio
RUN pip install pyAesCrypt


ADD . /
WORKDIR /
CMD python ACI_Project/aws_iot_pub.py 2> object.txt
