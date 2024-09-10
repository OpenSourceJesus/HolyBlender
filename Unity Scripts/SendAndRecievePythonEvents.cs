using UnityEngine;
using System.Collections;
using UnityEngine.Networking;

public class SendAndRecieveJsonEvents : MonoBehaviour
{
	public string jsonText;

	void OnEnable ()
	{
		StartCoroutine(JsonEvent ());
	}

	IEnumerator JsonEvent ()
	{
		UnityWebRequest webRequest = UnityWebRequest.Get("http://localhost:8000/exec?" + jsonText.Base64Encode());
		yield return webRequest.SendWebRequest();
		if (webRequest.result == UnityWebRequest.Result.Success)
			print("Web request result: " + webRequest.downloadHandler.text);
		else
			print(webRequest.error);
	}
}