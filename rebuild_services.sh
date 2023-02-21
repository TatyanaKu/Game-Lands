#!/bin/bash
cd services/land-management
. build_image.sh

cd ../../services/resource-management
. build_image.sh

cd ../../services/building-management
. build_image.sh

cd ../../services/user-service
. build_image.sh

cd ../../services/gameplay-configuration-manager
. build_image.sh

cd ../../services/resource-harvesting-service
. build_image.sh