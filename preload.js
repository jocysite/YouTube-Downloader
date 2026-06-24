const { contextBridge } = require("electron");

/**
 * Preload script for YouTube Downloader Desktop.
 * Exposes a safe API to the renderer process via contextBridge.
 */
contextBridge.exposeInMainWorld("electronAPI", {
  isDesktop: true,
  platform: process.platform,
});