#!/usr/bin/env bash
#!/usr/bin/env bash
set -e

build_this()
{
    local NAME_TAG=$1

    docker build -t $NAME_TAG .
    local TAG_PARTS=(${NAME_TAG//\// })
    docker images | grep ${TAG_PARTS[0]}
}
# build_this pick_three/pick_three:0.1.0
ssh_this()
{
    echo starting
    local NAME_TAG=$1
    local IMAGE_ID=$(docker images "$NAME_TAG" -q)
    echo "$IMAGE_ID"
    docker kill $(docker ps -q)


    docker run -dit -p 2222:22 -v /var/run/docker.sock:/var/run/docker.sock "$IMAGE_ID" && docker ps && ssh docker_base
}
# ssh_this pick_three/pick_three:0.1.0

clean_up_containers()
{
    # remove all the containers.
    docker rm $(docker ps -a -q)
    docker ps -all
}

aggressively_clean_up_images(){
    # remove everything without a corresponding container.
    docker image prune -a
    docker images
}

run_this()
{
    docker run -it pick_three/pick_three:0.1.0
}

attach_this()
{
    docker ps
    echo docker attach [id]
}

login_aws_docker()
{
    cat ~/.aws/credentials
    aws ecr get-login --no-include-email --region us-east-1 --profile prod
}

push_this()
{
    local TAG=$1

    docker tag tools_ui/tools_ui:"$TAG" $REPO_NAME_HERE/tools_ui:"$TAG"
    docker push $REPO_NAME_HERE/tools_ui:"$TAG"

}
# push_this 3.0.1

