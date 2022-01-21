# ./utils/downloader.py
# mv ./wp-core/wp-content ./wp-content

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac
echo ${machine}

if [ -x "$(command -v docker)" ]; then
    read -p "Project Name: " projectName
    read -p "Local Port: " openPort
    read -p "Database Username:" dbUser
    read -p "Database Password: " dbPassword

    # ./source_files/downloader.py -d -i backdrop-src
    # chmod 777 ./backdrop-src/settings.php
    # mv backdrop-src/files ./files 
    # mv backdrop-src/layouts ./layouts
    # mv backdrop-src/modules ./modules 
    # mv backdrop-src/sites ./sites 
    # mv backdrop-src/themes ./themes

else
    printf '%s\n' "Docker not found. Please install before continuing." >&2
    exit 1
fi

if [ machine=="Linux" ]
then
    sed -i "s/{wp-db}/$projectName/" docker-compose.yml
    sed -i "s/{wp-port}/$openPort/" docker-compose.yml
    sed -i "s/{wp-db-user}/$dbUser/" docker-compose.yml
    sed -i "s/{wp-pass}/$dbPassword/" docker-compose.yml
elif [ machine=="Mac"]
then
  echo "Mac not currently fully supported"
  echo "Please manually configure docker-compose.yml"
fi

docker-compose build
