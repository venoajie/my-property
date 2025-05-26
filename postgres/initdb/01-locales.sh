# postgres/initdb/01-locales.sh
#!/bin/bash
apk add --no-cache langpacks-en && \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8