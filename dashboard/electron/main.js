const { app, BrowserWindow } = require('electron');
const path = require('path');

const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;

function createWindow() {
  const win = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
    backgroundColor: '#1a1a1a',
  });

  if (isDev) {
    // Dev mode → load Next.js dev server
    win.loadURL('http://localhost:3000');
    win.webContents.openDevTools();
  } else {
    // Production mode → load built Next.js files
    win.loadFile(path.join(__dirname, '../dashboard/.next/server/pages/index.html'));
  }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
