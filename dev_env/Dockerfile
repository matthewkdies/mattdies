FROM ubuntu:22.04

ARG PYTHON_VERSION="3.11"
ARG USER=dev
ARG USER_HOME=/home/${USER}
ARG DEBIAN_FRONTEND=noninteractive

# setting lang recommended by Ubuntu image
# add local pipx bin directory to $PATH
ENV LANG=C.UTF-8 \
    PATH=${PATH}:${USER_HOME}/.local/bin:${USER_HOME}/.local/pipx/venvs/poetry/bin:/root/.local/bin \
    PYTHONBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=America/New_York \
    PYTHONPATH="${USER_HOME}/.local/pipx/venvs/poetry/lib/python${PYTHON_VERSION}/site-packages:/root/.local/bin"

# add python apt repo and install apt packages
RUN apt-get update \
    # create user and add to sudoers list
    && apt-get -y install sudo \
    && useradd --create-home --shell /bin/bash ${USER} \
    && echo "${USER} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USER} \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    curl \
    git \
    less \
    nano \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-distutils \
    python${PYTHON_VERSION}-venv \
    unzip \
    # clear apt lists
    && rm -rf /var/lib/apt/lists/* \
    # alias python and python3
    && alias python='python${PYTHON_VERSION}' \
    && alias python3='python${PYTHON_VERSION}' \
    # map python version installed to python and python3
    && ln --symbolic --force /usr/bin/python${PYTHON_VERSION} /usr/local/bin/python \
    && ln --symbolic --force /usr/bin/python${PYTHON_VERSION} /usr/local/bin/python3 \
    # install pip
    && curl -sSL https://bootstrap.pypa.io/get-pip.py | python - \
    # confirm python installation
    && python${PYTHON_VERSION} --version \
    && python${PYTHON_VERSION} -m pip --version \
    # install subrepo CLI tool
    && git clone https://github.com/ingydotnet/git-subrepo /usr/local/bin/git-subrepo \
    && chmod +x /usr/local/bin/git-subrepo/.rc \
    && echo 'source /usr/local/bin/git-subrepo/.rc' >> ${USER_HOME}/.bashrc \
    # create permissions on /usr/src; poetry uses this dir for git repos
    && mkdir -p /usr/src \
    && chown dev:dev /usr/src \
    && sudo chown ${USER} /root \
    # install pipx
    && python3 -m pip install --user pipx \
    # install dev tools with pipx
    && pipx install bandit \
    && pipx install black \
    && pipx install pylint \
    && pipx install poetry \
    && poetry config virtualenvs.create false \
    # create poetry cache directory
    && mkdir --parents ${USER_HOME}/.cache/pypoetry \
    && sudo chown ${USER} ${USER_HOME}/.cache/pypoetry -R \
    && mkdir /workspace

# mount poetry cache and set permissions in container
RUN --mount=type=cache,target=/var/cache/apt/archives \
    sudo chown --recursive 1000 /workspace 

CMD [ "sleep", "infinity" ]
