import PropTypes from 'prop-types';
import React from 'react';
import {StyleSheet, Text, TextStyle, View} from 'react-native';
import {StylePropType} from 'react-native-gifted-chat';

const {textStyle} = StyleSheet.create({
  textStyle: {
    fontSize: 16,
    lineHeight: 20,
    marginTop: 5,
    marginBottom: 5,
    marginLeft: 10,
    marginRight: 10,
  },
});
const styles = {
  left: StyleSheet.create({
    container: {},
    text: {
      color: 'black',
      ...textStyle,
    },
    link: {
      color: 'black',
      textDecorationLine: 'underline',
    },
  }),
  right: StyleSheet.create({
    container: {},
    text: {
      color: 'white',
      ...textStyle,
    },
    link: {
      color: 'white',
      textDecorationLine: 'underline',
    },
  }),
};
export function MyCustomMessageComponent({
  currentMessage = {},
  position = 'left',
  containerStyle,
  textStyle,
}) {
  // TODO: React.memo
  // const shouldComponentUpdate = (nextProps: MessageTextProps<TMessage>) => {
  //   return (
  //     !!currentMessage &&
  //     !!nextProps.currentMessage &&
  //     currentMessage.text !== nextProps.currentMessage.text
  //   )
  // }
  const textStyles: TextStyle =
    position === 'left' ? styles.left.text : styles.right.text;

  const sample =
    'Name: Kennedy King\nAge: 89\nBed Number: 49792\n\nVitals:\n- Temperature: 98\n- Pulse: 97\n- Respiration Rate: 21\n- Systolic Blood Pressure: 35\n- Diastolic Blood Pressure: 110\n- Oxygen Saturation: 90\n- Position: Standing';
  return (
    <View
      style={[
        textStyle && textStyle,
        containerStyle && containerStyle[position],
      ]}>
      {/*<Markdown style={{text: {...textStyle}}}>{sample}</Markdown>*/}
      {/*<Markdown style={{text: {...textStyle}}}>{currentMessage?.text}</Markdown>*/}
      <Text style={{...textStyle}}>{currentMessage?.text}</Text>
    </View>
  );
}
MyCustomMessageComponent.propTypes = {
  position: PropTypes.oneOf(['left', 'right']),
  currentMessage: PropTypes.object,
  containerStyle: PropTypes.shape({
    left: StylePropType,
    right: StylePropType,
  }),
  textStyle: PropTypes.shape({
    left: StylePropType,
    right: StylePropType,
  }),
};
//# sourceMappingURL=MessageText.js.map
