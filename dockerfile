FROM ubuntu
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install pywebio
RUN pip3 install asyncio
COPY chatsrv.py /home/
EXPOSE 8080
CMD ["python3","/home/chatsrv.py"]
