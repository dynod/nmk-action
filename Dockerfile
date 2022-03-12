# Use python image
FROM python:3.7

COPY entrypoint.sh /

# Go through entry point
ENTRYPOINT [ "/entrypoint.sh" ]
