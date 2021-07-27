# uvicorn main:app --port 38080 --workers 2 --preload

# https://www.uvicorn.org/#running-with-gunicorn
# https://docs.gunicorn.org/en/stable/settings.html#preload-app
# https://stackoverflow.com/questions/45071875/memory-sharing-among-workers-in-gunicorn-using-preload

gunicorn main:app --bind=localhost:38080 \
                  --workers=2 \
                  --preload \
                  --worker-class=uvicorn.workers.UvicornWorker
