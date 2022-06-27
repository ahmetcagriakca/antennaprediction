FROM        ahmetcagriakca/antenna-prediction:base

RUN         pip3 install --upgrade pip
COPY       	./requirements.txt /app/requirements.txt
WORKDIR    	/app

RUN 		pip3 install -r requirements.txt 
RUN         pip3 list -i $PIP_URL_PRIVATE

COPY       	. /app
WORKDIR    	/app

# # openshift set permission to non-root users for /app directory
# RUN chgrp -R 0 /app && \
#     chmod -R g=u /app

# # openshift set running user 
# USER 1001
ENTRYPOINT 	["python3"]
CMD 		["startup.py"]