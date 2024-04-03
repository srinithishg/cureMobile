// import React, {useState} from 'react';
// import {GiftedChat} from 'react-native-gifted-chat';
// import {
//   Button,
//   Image,
//   Linking,
//   StyleSheet,
//   Text,
//   TouchableOpacity,
//   View,
// } from 'react-native';
//
// const styles = StyleSheet.create({
//   webview: {
//     flex: 3,
//   },
//   link: {
//     color: 'blue',
//     textAlign: 'center',
//     marginVertical: 10,
//   },
// });
// export function Example({navigation}: any) {
//   const [messages, setMessages] = useState([
//     {
//       _id: 1,
//       text: 'Hello! I am your chatbot. How can I help you?',
//       createdAt: new Date(),
//       user: {
//         _id: 2,
//         name: 'Chatbot',
//       },
//     },
//   ]);
//   const handleLinkPress = (url: any) => {
//     // Open the WebView screen
//     navigation.navigate('WebViewScreen', {url});
//     Linking.openURL(
//       'https://gcp-qa.emr.cure.org/bahmni/home/index.html#/login',
//     );
//   };
//   const handleSend = (newMessages = []) => {
//     setMessages(previousMessages =>
//       GiftedChat.append(previousMessages, newMessages),
//     );
//
//     const userMessage = newMessages[0].text;
//     const botResponse = generateChatbotResponse(userMessage);
//
//     const m = (previousMessages: any) =>
//       GiftedChat.append(previousMessages, [
//         {
//           _id: Math.round(Math.random() * 1000000),
//           text: botResponse.text,
//           createdAt: new Date(),
//           user: {
//             _id: 2,
//             name: 'Chatbot',
//           },
//           botResponse,
//         },
//       ]);
//     setMessages(previousMessages => m(previousMessages));
//   };
//
//   const generateChatbotResponse = (userMessage: any) => {
//     switch (userMessage.toLowerCase()) {
//       case 'hello':
//         return {
//           component: 'String',
//           text: 'Hi there! How can I assist you today?',
//         };
//       case 'buttons':
//         return {
//           component: (
//             <>
//               <Button
//                 title={'Click Me'}
//                 onPress={() => console.log('Button clicked!')}
//               />
//             </>
//           ),
//           text: 'Buttons',
//         };
//       case 'image':
//         return {
//           component: (
//             <>
//               <Image
//                 source={require('./img.png')}
//                 style={{width: 100, height: 100}}
//               />
//             </>
//           ),
//           text: 'Image',
//         };
//       case 'link':
//         return {
//           component: (
//             <>
//               <TouchableOpacity onPress={() => console.log('Link pressed!')}>
//                 <Text style={{color: 'blue', textDecorationLine: 'underline'}}>
//                   Click here
//                 </Text>
//               </TouchableOpacity>
//             </>
//           ),
//           text: 'Link',
//         };
//       case 'webview':
//         return {
//           component: (
//             <>
//               <View>
//                 <TouchableOpacity
//                   onPress={() => handleLinkPress('https://www.bahmni.org/')}>
//                   <Text style={styles.link}>Open WebView</Text>
//                 </TouchableOpacity>
//               </View>
//             </>
//           ),
//           text: 'Webview',
//         };
//       default:
//         return {
//           component: (
//             <>
//               <Image
//                 source={require('./img.png')}
//                 style={{width: 100, height: 100}}
//               />
//             </>
//           ),
//           text: "I'm sorry, I didn't understand that. Can you please rephrase?",
//         };
//     }
//   };
//
//   const MyComponent = (props: any) => {
//     const {currentMessage} = props;
//     const {text, botResponse} = currentMessage;
//
//     console.log('sample', botResponse);
//     return (
//       <View
//         style={{
//           minHeight: 20,
//           alignItems: 'center',
//           padding: 10,
//         }}>
//         <Text>{text}</Text>
//         {botResponse && botResponse.component}
//       </View>
//     );
//   };
//
//   return (
//     <View
//       style={{
//         flex: 1,
//         backgroundColor: '#d8d8d8',
//       }}>
//       <GiftedChat
//         messages={messages}
//         onSend={(newMessages: any) => handleSend(newMessages)}
//         user={{_id: 1, name: 'User'}}
//         renderMessageText={props => <MyComponent {...props} />}
//       />
//     </View>
//   );
// }
