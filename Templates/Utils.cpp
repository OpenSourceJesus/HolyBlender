#include "Utils.h"
#include <stdio.h>
#include "Camera/PlayerCameraManager.h"
#include "Templates/SharedPointer.h"

Utils::Utils ()
{
}

FVector Utils::GetMousePosition (UWorld* world)
{
	double x;
	double y;
	UGameplayStatics::GetPlayerController(world, 0)->GetMousePosition(x, y);
	return FVector(x, y, 0);
}

FVector Utils::ScreenToWorldPoint (UWorld* world, FVector screenPoint)
{
	FVector output;
	FVector direction;
	UGameplayStatics::DeprojectScreenToWorld(UGameplayStatics::GetPlayerController(world, 0), ToVec2D(screenPoint), output, direction);
	return output;
}

// FVector Utils::GetMousePositionWorld (UWorld* world)
// {
// 	return ScreenToWorldPoint(world, GetMousePosition(world));
// }

AActor* Utils::SpawnActor (UWorld* world, AActor actor, FVector location, FRotator rotation)
{
	AActor* output = world->SpawnActor(actor.StaticClass(), TSharedPtr<const FVector>(&location).Get(), TSharedPtr<const FRotator>(&rotation).Get(), FActorSpawnParameters());
	return output;
}

FVector2D Utils::ToVec2D (FVector v)
{
	return FVector2D(v.X, v.Y);
}

// AActor Utils::GetActor (FString name, UWorld* world)
// {
// 	for (TActorIterator<AActor> actor(world); actor; ++ actor)
// 	{
// 			return actor;
// 	}
// 	// throw new std::exception();
// 	return nullptr;
// }