metahosting-worker-status
=========================

[![Build Status](https://travis-ci.org/BeneDicere/metahosting-worker-status.svg?branch=master)](https://travis-ci.org/BeneDicere/metahosting-worker-status)

Component that is launched as a container on the metahosting-worker and utilizing
[cadvisor](https://github.com/google/cadvisor) to collect resource utilization,  
report it to the messaging system and with this a monitoring frontend for admins

To get an running environment, see docker-compose.yml. Especially the external-link for the messaging container is important.