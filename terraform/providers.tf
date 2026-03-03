terraform {
  required_version = ">= 1.0.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {
  # هذا السطر يخبر Terraform بالتواصل مع Docker المثبت على جهازك الـ Ubuntu
  host = "unix:///var/run/docker.sock"
}