# syntax=docker/dockerfile:1
# Locked-environment pattern adapted from CBIO7501 lesson 08 (see NOTICE).
ARG PIXI_IMAGE=ghcr.io/prefix-dev/pixi:0.83.0@sha256:fbb7e74827c5f703782f68afb027cb70f6273707d0db8155c53aa66e9de5e1e6

FROM ${PIXI_IMAGE} AS build
WORKDIR /opt/capstone
COPY pixi.toml pixi.lock ./
RUN pixi install --locked --environment default \
    && pixi install --locked --environment workflow \
    && printf '%s\n' '#!/bin/bash' 'set -e' > /entrypoint.sh \
    && pixi shell-hook --locked --environment default --shell bash >> /entrypoint.sh \
    && printf '%s\n' 'exec "$@"' >> /entrypoint.sh

FROM ${PIXI_IMAGE}
# Keep both installation prefixes. The workflow and analysis use different Python versions.
COPY --from=build /opt/capstone/.pixi/envs/ /opt/capstone/.pixi/envs/
COPY --from=build --chmod=0755 /entrypoint.sh /entrypoint.sh
ENV CAPSTONE_ANALYSIS_BIN=/opt/capstone/.pixi/envs/default/bin
ENV PATH=$CAPSTONE_ANALYSIS_BIN:$PATH
# Snakemake logs the username even when the host UID has no passwd entry here.
ENV USER=capstone

# Mount the checkout here to keep inputs, results and the report on the host.
WORKDIR /work
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash", "-c", "python scripts/download_data.py && exec /opt/capstone/.pixi/envs/workflow/bin/snakemake --snakefile workflow/Snakefile --cores 1 --rerun-incomplete"]
