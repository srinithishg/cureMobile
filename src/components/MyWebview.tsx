import React from 'react';
import {StyleSheet} from 'react-native';
import WebView from 'react-native-webview';

const MyWebView = () => {
  return (
    <>
      <WebView
        source={{uri: 'https://gcp-qa.emr.cure.org/bahmni/home/index.html#/dashboard'}}
        style={styles.webview}
      />
    </>
  );
};

const styles = StyleSheet.create({
  webview: {
    flex: 3,
  },
  link: {
    color: 'blue',
    textAlign: 'center',
    marginVertical: 10,
  },
});

export default MyWebView;
