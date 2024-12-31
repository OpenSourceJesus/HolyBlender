// using Extensions;
// using UnityEngine;
// using UnityEngine.Networking;
// #if UNITY_EDITOR
// using UnityEditor;
// #endif

// namespace HolyBlender
// {
// 	public class MakeTexture2DAssetFromURL : MakeAsset
// 	{
// 		public string imageURL;
// 		public Texture2D texture;
// 		UnityWebRequest imageRequest;

// 		public override void Do ()
// 		{
// 			if (imageRequest == null)
// 			{
// 				imageRequest = UnityWebRequest.Get(imageURL);
// 				imageRequest.SendWebRequest();
// 			}
// 			else if (imageRequest.isDone)
// 			{
// 				print(imageRequest.downloadHandler.text);
// 				texture = new Texture2D(1, 1);
// 				if (ImageConversion.LoadImage(texture, imageRequest.downloadHandler.data))
// 				{
// 					obj = texture;
// 					base.Do ();
// 					print("Success");
// 				}
// 				else
// 				{
// 					print(imageRequest.error.ToString());
// 					print("No");
// 				}
// 				doRepeatedly = false;
// 				EditorApplication.update -= Do;
// 			}
// 		}
// 	}
// }