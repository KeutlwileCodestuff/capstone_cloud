import Amplify from 'aws-amplify';

Amplify.configure({
    Auth: {
      region: 'eu-west-1',
      userPoolId: 'eu-west-1_E5nih2JQ3',
      userPoolWebClientId: '2r31k2an842dokhk7uvnard1kl'
    },

    API: {
      endpoints: [
        {
          name: 'Serverless-convenient-self-storage-API',
          endpoint: 'https://9m8bcav2ui.execute-api.eu-west-1.amazonaws.com/Prod',
          region: 'eu-west-1'
        }
      ]
    }
  });