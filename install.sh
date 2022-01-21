./utils/downloader.py
mv ./wp-core/wp-content ./wp-content

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
  echo "Please verify docker-compose.yml"
  sed -i'' -e "s/{wp-db}/$projectName/g" docker-compose.yml
  sed -i'' -e "s/{wp-port}/$openPort/g" docker-compose.yml
  sed -i'' -e "s/{wp-db-user}/$dbUser/g" docker-compose.yml
  sed -i'' -e "s/{wp-pass}/$dbPassword/g" docker-compose.yml
fi

docker-compose build
