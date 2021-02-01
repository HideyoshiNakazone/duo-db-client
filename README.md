<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** HideyoshiNakazone, duo-db-client, NakazoneVitor, vitor.h.n.batista@gmail.com, project_title, project_description
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">Duo DB Client</h3>

  <p align="center">
    Python script to integratee PostgreSQL with Email and Google Calendar
    <br />
    <br />
    <a href="https://github.com/HideyoshiNakazone/duo-db-client/issues">Report Bug</a>
    ·
    <a href="https://github.com/HideyoshiNakazone/duo-db-client/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a simple python script that listens for PostgreSQL notification and send emails and create Google Cadendar events based in the informations inserted into to the PostgreSQL database.


### Built With

* [Python 3](https://www.python.org/download/releases/3.0/)
* [PostgreSQL](https://www.postgresql.org/)

<!-- GETTING STARTED -->
## Getting Started

To use the script you first have to create a PostgreSQL database and insert the database information into the script (Host Adress, Port, Server Name, Database Name, User Name and Password for the database admin).

### Prerequisites

* [Pip](https://pypi.org/project/pip/)
* [Psycopg2](https://www.psycopg.org/docs/)
* [google-api-python-client](https://github.com/googleapis/google-api-python-client)
* [google_auth_oauthlib](https://pypi.org/project/google-auth-oauthlib/)

This is an list things you need to use the software and how to install them.

* Psycopg2

  ```sh
  pip install psycopg2-binary
  ```
* Google API and Google Outh

  ```sh
  pip install google-api-python-client
  ```
  ```sh
  pip install google_auth_oauthlib
  ```

### Installation

The only installation method is cloning the repo
   ```sh
   git clone https://github.com/HideyoshiNakazone/duo-db-client.git
   ```

<!-- USAGE EXAMPLES -->
## Usage

For any pratical use of the script you will have set your Google API Credentials and to modify the script to make queries usefull to yourself, these queries will have to be made in postgres and for more examples, please refer to the [Psycopg2 Documentation](https://www.psycopg.org/docs/)

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Your Name - [@NakazoneVitor](https://twitter.com/NakazoneVitor) - vitor.h.n.batista@gmail.com

Project Link: [https://github.com/HideyoshiNakazone/duo-db-client](https://github.com/HideyoshiNakazone/duo-db-client)

#

README file made using https://github.com/othneildrew/Best-README-Template

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/HideyoshiNakazone/duo-db-client.svg?style=for-the-badge
[contributors-url]: https://github.com/HideyoshiNakazone/duo-db-client/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/HideyoshiNakazone/duo-db-client.svg?style=for-the-badge
[forks-url]: https://github.com/HideyoshiNakazone/duo-db-client/network/members
[stars-shield]: https://img.shields.io/github/stars/HideyoshiNakazone/duo-db-client.svg?style=for-the-badge
[stars-url]: https://github.com/HideyoshiNakazone/duo-db-client/stargazers
[issues-shield]: https://img.shields.io/github/issues/HideyoshiNakazone/duo-db-client.svg?style=for-the-badge
[issues-url]: https://github.com/HideyoshiNakazone/duo-db-client/issues
[license-shield]: https://img.shields.io/github/license/HideyoshiNakazone/duo-db-client.svg?style=for-the-badge
[license-url]: https://github.com/HideyoshiNakazone/duo-db-client/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/HideyoshiNakazone
