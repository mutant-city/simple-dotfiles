if ! [ -x "$(command -v /usr/bin/ruby)" ]; then
  exit 1
fi

if ! [ -x "$(command -v curl)" ]; then
  exit 1
fi

exit 0