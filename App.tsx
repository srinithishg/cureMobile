import React from 'react';
import {
  Dimensions,
  SafeAreaView,
  StatusBar,
  useColorScheme,
  View,
} from 'react-native';
import {NavigationContainer} from '@react-navigation/native';
import {Colors} from 'react-native/Libraries/NewAppScreen';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import {CureSmart} from './src/components/CureSmart.tsx';

const Stack = createNativeStackNavigator();
function App(): React.JSX.Element {
  const isDarkMode = useColorScheme() === 'dark';
  const screenWidth = Dimensions.get('window').width;

  return (
    <NavigationContainer>
      <SafeAreaView
        style={{
          flex: 1,
          justifyContent: 'center',
          alignItems: 'center',
          backgroundColor: !isDarkMode ? 'black' : 'white',
        }}>
        <StatusBar
          barStyle={!isDarkMode ? 'light-content' : 'dark-content'}
          backgroundColor={isDarkMode ? Colors.darker : Colors.lighter}
        />
        <View
          style={{
            flex: 1,
            width: screenWidth,
          }}>
          <Stack.Navigator>
            <Stack.Screen
              name="Cure Smart"
              component={CureSmart}
              options={{
                headerStyle: {backgroundColor: 'black'},
                headerTintColor: 'white',
              }}
            />
          </Stack.Navigator>
        </View>
      </SafeAreaView>
    </NavigationContainer>
  );
}

export default App;
