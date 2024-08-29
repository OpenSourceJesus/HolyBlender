using UnityEngine;
using System.Collections;
using UnityEngine.Networking;

public class SendAndRecieveClickEvent : MonoBehaviour
{
	void Update ()
	{
		if (Input.GetMouseButtonDown(0))
		{
			Ray ray = Camera.main.ScreenPointToRay();
			RaycastHit hit;
			if (Physics.Raycast(ray.origin, ray.direction, out hit, Mathf.Infinity, LayerMask.GetMask("Clickable"), QueryTriggerInteraction queryTriggerInteraction = QueryTriggerInteraction.Collide))
			{
				UnityWebRequest webRequest = UnityWebRequest.Post("", string postData, string contentType);
				yield return webRequest.SendWebRequest();
				if (webRequest.result == UnityWebRequest.Result.Success)
					print("Web request result: " + webRequest.downloadHandler.text);
				else
					print(webRequest.error);
			}
		}
	}
}