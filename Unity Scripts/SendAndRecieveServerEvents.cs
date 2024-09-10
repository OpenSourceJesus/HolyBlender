using UnityEngine;
using System.Collections;
using UnityEngine.Networking;

public class SendAndRecieveServerEvents : MonoBehaviour
{
	public string jsonText;

	void OnEnable ()
	{
		StartCoroutine(JsonEvent (jsonText));
	}

	void Update ()
	{
		if (Input.GetMouseButtonDown(0))
		{
			Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
			RaycastHit hit;
			if (Physics.Raycast(ray.origin, ray.direction, out hit, Mathf.Infinity, 1 << 31, QueryTriggerInteraction.Collide))
				StartCoroutine(OnClickEvent (hit.collider.name));
		}
	}

	IEnumerator OnClickEvent (string objectName)
	{
		UnityWebRequest webRequest = UnityWebRequest.Get("http://localhost:8000/" + objectName);
		yield return webRequest.SendWebRequest();
		if (webRequest.result == UnityWebRequest.Result.Success)
			print("Web request result: " + webRequest.downloadHandler.text);
		else
			print(webRequest.error);
	}


	IEnumerator JsonEvent (string jsonText)
	{
		UnityWebRequest webRequest = UnityWebRequest.Get("http://localhost:8000/exec?" + jsonText.Base64Encode());
		yield return webRequest.SendWebRequest();
		if (webRequest.result == UnityWebRequest.Result.Success)
			print("Web request result: " + webRequest.downloadHandler.text);
		else
			print(webRequest.error);
	}
}