installwordpress
=========

From williamyeh ansible workshop Example

Requirements
------------

nginx, mysql, php-fpm

Role Variables
--------------

vars/main.yml

Dependencies
------------

williamyeh.nginx

geerlingguy.mysql

theqwan-chengwei.ubuntuphpfpm7


Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - theqwan-chengwei.installwordpress

License
-------

BSD

