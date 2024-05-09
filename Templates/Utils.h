#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Kismet/GameplayStatics.h"
#include "PackedLevelActor/PackedLevelActor.h"

class BAREUEPROJECT_API Utils
{
public:	
	Utils ();
	static FVector GetMousePosition (UWorld* world);
	static FVector ScreenToWorldPoint (UWorld* world, FVector screenPoint);
	// static FVector GetMousePositionWorld (UWorld* world);
	static AActor* SpawnActor (UWorld* world, AActor actor, FVector position, FRotator rotation);
	static FVector2D ToVec2D (FVector v);
	template<typename T> static T GetRootActorInLevel (ULevel* level)
	{
		return (T) level->Actors[0];
	}
};