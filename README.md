# wordpress_dockerized
Fancy Wordpress container for developing plugins and themes.

## System Requirements
* Docker
* Linux
* Python 3.x

Not currently tested on Mac or Windows machines.

## Installation
Run `./install.sh` in the terminal to set download wordpress files and set up project details.

The install script will ask you for various project information to set up the `docker-compose.yml` file with.

After set up run `docker-compose up` in the terminal to launch the project.

Use the port number you set up to visit the project in the browser at localhost:[your port number]

Enter in the database connection details on the wordpress installation screen.

**Notice:** The database default location is localhost and will not work. Use your project name as the database address. This is listed under `volumes:` at the end of docker-compose.yml if you've forgotten it.

## License
MIT