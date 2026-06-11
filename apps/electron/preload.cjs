const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("desktopApi", {
  selectDirectory: (title) => ipcRenderer.invoke("dialog:selectDirectory", title),
  backendRequest: (route, options) => ipcRenderer.invoke("backend:request", route, options)
});
