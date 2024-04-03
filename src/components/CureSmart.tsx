import React, {useEffect, useState} from 'react';
import {Bubble, GiftedChat, Send} from 'react-native-gifted-chat';
import {
  ActivityIndicator,
  Image,
  ImageBackground,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import axios from 'axios';
import {MyCustomMessageComponent} from './MyCustomMessageComponent.tsx';

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
export function CureSmart() {
  const [messages, setMessages] = useState([]);
  const [backGround, setBackGround] = useState(true);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (messages.length > 0) {
      setBackGround(false);
    } else {
      setBackGround(true);
    }
  }, [messages]);
  const getAiResponse = async (userQuestion: string) => {
    try {
      setLoading(true);
      const [latestMessage, previousMessage] = messages
        .slice(0, 2)
        .map(message => message.text);

      let requestData = {
        message: userQuestion,
      };
      if (previousMessage) {
        requestData = {
          ...requestData,
          previous_question: previousMessage,
        };
      }
      if (latestMessage) {
        requestData = {
          ...requestData,
          previous_answer: latestMessage,
        };
      }

      const response = await axios.post(
        'https://0391-2401-4900-1ce2-e5fa-803b-e670-e043-ec85.ngrok-free.app/bahmni/rest/v1/conversations',
        {
          ...requestData,
          provider: 'Laurence Wicks',
        },
      );
      return response.data;
    } catch (error) {
      console.error(error);
      return {
        message:
          "Hey, I'm still learning. Could you please provide more context to help me assist you further?",
      };
    } finally {
      setLoading(false);
    }
  };

  const onHandleInput = (text: string) => {
    if (text.length > 0) {
      setBackGround(false);
    } else if (messages.length === 0) {
      setBackGround(true);
    }
  };
  const handleSend = async (newMessages = []) => {
    setMessages(previousMessages =>
      GiftedChat.append(previousMessages, newMessages),
    );

    const userMessage = newMessages[0].text;
    const botResponse = await getAiResponse(userMessage);
    const appendBotResponse = (previousMessages: any) => {
      const newBotMessage = {
        _id: Math.round(Math.random() * 1000000),
        text: botResponse.message,
        createdAt: new Date(),
        user: {
          _id: 2,
          name: 'CureSmart',
          avatar: require('../assets/botAvatar.png'),
        },
      };
      return GiftedChat.append(previousMessages, [newBotMessage]);
    };

    setMessages(previousMessages => appendBotResponse(previousMessages));
  };

  const MyComponent = (props: any) => {
    const {currentMessage} = props;

    const textStyle =
      props.position === 'left' ? styles.left.text : styles.right.text;
    return (
      <MyCustomMessageComponent
        {...props}
        currentMessage={currentMessage}
        textStyle={textStyle}
      />
    );
  };

  const MySend = (props: any) => {
    return (
      <Send {...props}>
        <Image
          style={{width: 48, height: 48}}
          source={require('../assets/send.png')}
          resizeMode={'contain'}
        />
      </Send>
    );
  };

  return (
    <View style={{flex: 1}}>
      <ImageBackground
        source={require('../assets/background.png')}
        resizeMode={'cover'}
        style={{
          position: 'absolute',
          top: 0,
          bottom: 0,
          left: 0,
          right: 0,
          zIndex: 0,
          opacity: backGround ? 100 : 0,
          backgroundColor: 'lightgray',
        }}>
        {backGround && (
          <View
            style={{flex: 1, alignItems: 'center', justifyContent: 'center'}}>
            <Text
              style={{
                fontFamily: 'IBMPlexSans',
                fontSize: 21,
                fontWeight: '600',
                lineHeight: 20,
                textAlign: 'center',
                color: 'black',
              }}>
              Hello! Laurence Wicks
            </Text>
            <Text
              style={{
                fontFamily: 'IBMPlexSans',
                fontSize: 14,
                fontWeight: '400',
                lineHeight: 20,
                textAlign: 'center',
                color: 'black',
              }}>
              How may I help you today?
            </Text>
          </View>
        )}
      </ImageBackground>
      <GiftedChat
        messages={messages}
        messagesContainerStyle={{
          zIndex: 10,
        }}
        onSend={(newMessages: any) => handleSend(newMessages)}
        user={{_id: 1, name: 'You'}}
        onInputTextChanged={text => onHandleInput(text)}
        renderMessageText={props => <MyComponent {...props} />}
        renderFooter={() =>
          loading && (
            <ActivityIndicator
              size="large"
              color="#007D79"
              style={{padding: 10}}
            />
          )
        }
        alwaysShowSend={true}
        textInputProps={{height: 48, margin: 0, color: 'black'}}
        placeholder={'Make your request here'}
        renderSend={props => <MySend {...props} />}
        scrollToBottom={true}
        renderBubble={props => {
          return (
            <Bubble
              {...props}
              wrapperStyle={{
                right: {
                  backgroundColor: '#007D79',
                },
                left: {
                  backgroundColor: 'white',
                },
              }}
            />
          );
        }}
      />
    </View>
  );
}
