// react-mic.d.ts

declare module 'react-mic' {
    import * as React from 'react';
  
    export interface ReactMicProps {
      record: boolean;
      className?: string;
      onStop: (recordedBlob: { blob: Blob; blobURL: string }) => void;
      burstTime?: number;
      mimeType?: string;
      echoCancellation?: boolean;
      noiseSuppression?: boolean;
      sampleRate?: number;
      bitRate?: number;
      channelCount?: number;
      backgroundColor?: string;
      strokeColor?: string;
      visualSetting?: 'frequencyBars' | 'sinewave';
      // Add any additional props as needed
    }
  
    export class ReactMic extends React.Component<ReactMicProps> {}
  }