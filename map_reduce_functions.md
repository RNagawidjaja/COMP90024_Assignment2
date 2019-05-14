# Map Reduce Functions #

## Gluttony ##
### Map ###
```
function (doc) {
  if (doc.geo != null && doc.lga_id !== undefined && doc.lga_id != null && doc.topic !== undefined && doc.topic.length && doc.topic[0] === 'gluttony'){
    emit([doc.lga_id,doc.topic[0]] , 1);
  }
}
```
### Reduce ###
```
_count
```

## Gluttony Rate ##
### Map ###
```
function (doc) {
  if (doc.geo != null && doc.lga_id !== undefined && doc.lga_id != null){
    if(doc.topic[0] === "gluttony"){
    emit(doc.lga_id , 1);
    }
    else{
      emit(doc.lga_id, 0)
    }
  }
}
```
### Reduce ###
```
_stats
```

## LGA ##
### Map ###
```
function (doc) {
  if (doc.geo != null && doc.lga_id !== undefined && doc.lga_id != null){
    emit(doc.lga_id, 1);
  }
}
```
### Reduce ###
```
_count
```

## Sloth ##
### Map ###
```
function (doc) {
  if (doc.geo != null && doc.lga_id !== undefined && doc.lga_id != null && doc.topic !== undefined && doc.topic.length && doc.topic[0] === 'sloth'){
    emit([doc.lga_id,doc.topic] , 1);
  }
}
```
### Reduce ###
```
_count
```

## Sloth Rate ##
### Map ###
```
function (doc) {
  if (doc.geo != null && doc.lga_id !== undefined && doc.lga_id != null){
    if(doc.topic[0] === "sloth"){
    emit(doc.lga_id , 1);
    }
    else{
      emit(doc.lga_id, 0)
    }
  }
}
```
### Reduce ###
```
_stats
```
