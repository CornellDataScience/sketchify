export interface IElectronAPI {
  [key: string]: any;
}

declare global {
  interface Window {
    electronAPI: IElectronAPI;
  }
}
