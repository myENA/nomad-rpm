# RPM Spec for Nomad

RPM build for creating [Nomad](https://www.nomadproject.io) packages for use in the ENA environment.

# Building

The RPMs may be built with [Docker](#with-docker), [Vagrant](#with-vagrant), or [manual](#manual).

Whatever way you choose you will need to do a few basic things first.

```bash
git clone https://github.com/myENA/nomad-rpm  ## check out this code
cd nomad-rpm                                  ## uhh... you should know
mkdir -p artifacts                            ## prep the artifacts location
```

## With Docker

```bash
docker build -t ena/nomad-rpm .                                ## build the image
docker run -v $PWD/artifacts:/tmp/artifacts -it ena/nomad-rpm  ## run the image and build the RPMs
```

## With Vagrant

```bash
vagrant up       ## provision and build the RPMs
```

## Manual

```bash
cat build.sh     ## read the script
```

## Result

Two RPMs will be copied into the `artifacts` folder:
1. `nomad-<version>-<release>.el7.centos.x86_64.rpm`         - The binary and systemd service definition (required)
2. `nomad-config-<version>-<release>.el7.centos.x86_64.rpm`  - Example agent configuration (recommended)

# Running

1. Install the RPM(s) that you need
2. Review and edit (if needed) `/etc/sysconfig/nomad` and associated config under `/etc/nomad.d/*` (config package)
3. Start the service and tail the logs: `systemctl start nomad.service` and `journalctl -f --no-pager -u nomad`
4. Optionally start on reboot with: `systemctl enable nomad.service`

## Configuring

Config files are loaded in lexicographical order from the `config` specified in `/etc/sysconfig/nomad` (config package).
You may modify and/or add to the provided configuration as needed.

# Further reading

See the [nomadproject.io](https://www.nomadproject.io) website.
