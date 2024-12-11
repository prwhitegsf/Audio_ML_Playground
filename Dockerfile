FROM continuumio/miniconda3

WORKDIR /Audio_ML_Playground

# Create the environment:
COPY environment.yml entrypoint.sh wsgi.py config.py app.db ./
COPY app app

RUN conda env create -f environment.yml --prefix ./ml_env &&\
    echo "conda activate ./ml_env" >> ~/.bashrc &&\
    chmod +x entrypoint.sh


# Make RUN commands use the new environment:
#RUN echo "conda activate ml_env" >> ~/.bashrc &&\

SHELL ["/bin/bash", "--login", "-c"]

# Demonstrate the environment is activated:
#RUN echo "Make sure flask is installed:"
#RUN python -c "import flask"

# The code to run when container is started:
ENV FLASK_APP=wsgi.py

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]





