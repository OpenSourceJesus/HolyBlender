#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"

class BAREUEPROJECT_API Utils
{
public:	
	Utils ();
	static FVector GetMousePosition (UWorld* world);
	static FVector ScreenToWorldPoint (UWorld* world, FVector screenPoint);
	// static FVector GetMousePositionWorld (UWorld* world);
	// static AActor* SpawnActor (UWorld* world, FString assetPath, FVector position, FRotator rotation);
	static FVector2D ToVec2D (FVector v);
	// static AActor GetActor (FString name, UWorld* world);
	template<typename T> static T GetRootActorInLevel (ULevel* level)
	{
		return (T) level->Actors[0];
	}
	// template<typename T> static void GetAllActors (UWorld* world, TArray<T*>& output)
	// {
	// 	for (TActorIterator<T> actor(world); actor; ++ actor)
	// 		output.Add(*actor);
	// }
};