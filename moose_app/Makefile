MOOSE_DIR ?= $(abspath ../.agent-runtime/moose)
FRAMEWORK_DIR ?= $(MOOSE_DIR)/framework
include $(FRAMEWORK_DIR)/build.mk
include $(FRAMEWORK_DIR)/moose.mk
APPLICATION_DIR := $(shell pwd)
APPLICATION_NAME := anisotropic_biot
BUILD_EXEC := yes
GEN_REVISION := no
include $(FRAMEWORK_DIR)/app.mk
