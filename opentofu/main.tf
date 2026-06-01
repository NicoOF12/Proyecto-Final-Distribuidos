terraform {
  required_providers {
    incus = {
      source  = "lxc/incus"
      version = "1.1.0"
    }
  }
}

resource "incus_instance" "node_control" {

  name = "node-control"

  image = "images:ubuntu/24.04"

  config = {
    "boot.autostart"   = "true"
    "security.nesting" = "true"
  }

  device {
    name = "eth0"

    type = "nic"

    properties = {
      "network"      = "ovn-lab"
      "ipv4.address" = "10.10.0.5"
    }
  }
}

resource "incus_instance" "app_api" {

  name = "app-api"

  image = "images:ubuntu/24.04"

  config = {
    "boot.autostart"   = "true"
    "security.nesting" = "true"
  }

  device {
    name = "eth0"

    type = "nic"

    properties = {
     "network"      = "ovn-lab"
      "ipv4.address" = "10.10.0.10"
    }
  }
}

resource "incus_instance" "app_core" {

  name = "app-core"

  image = "images:ubuntu/24.04"

  config = {
    "boot.autostart"   = "true"
    "security.nesting" = "true"
  }

  device {
    name = "eth0"

    type = "nic"

    properties = {
      "network"      = "ovn-lab"
      "ipv4.address" = "10.10.0.11"
    }
  }
}

resource "incus_instance" "db_postgres" {

  name = "db-postgres"

  image = "images:ubuntu/24.04"

  config = {
    "boot.autostart"   = "true"
    "security.nesting" = "true"
  }

  device {
    name = "eth0"

    type = "nic"

    properties = {
      "network"      = "ovn-lab"
      "ipv4.address" = "10.10.0.12"
    }
  }
}

resource "incus_instance" "monitoring" {

  name = "monitoring"

  image = "images:ubuntu/24.04"

  config = {
    "boot.autostart"   = "true"
    "security.nesting" = "true"
  }

  device {
    name = "eth0"

    type = "nic"

    properties = {
      "network"      = "ovn-lab"
      "ipv4.address" = "10.10.0.20"
    }
  }
}

resource "incus_instance" "ceph_node" {

  name = "ceph-node"

  image = "images:ubuntu/24.04"

  config = {
    "boot.autostart"   = "true"
    "security.nesting" = "true"
  }

  device {
    name = "eth0"

    type = "nic"

    properties = {
      "network"      = "ovn-lab"
      "ipv4.address" = "10.10.0.30"
    }
  }
}
