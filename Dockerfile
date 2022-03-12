# Use python image
FROM python:3.10

COPY entrypoint.sh /

# Go through entry point
ENTRYPOINT [ "/entrypoint.sh" ]
