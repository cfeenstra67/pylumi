package pylumi

import (
    "encoding/json"
    "fmt"

    "github.com/pulumi/pulumi/sdk/v2/go/common/resource"
    "github.com/pulumi/pulumi/sdk/v2/go/common/resource/plugin"
)


const (
    UnknownKey = "$unknown"
    UnknownNullValue = ""
)


// Copied from the `plugin` module
func unmarshalUnknownPropertyValue(s string) (resource.PropertyValue, bool) {
    var elem resource.PropertyValue
    var unknown bool
    switch s {
    case plugin.UnknownBoolValue:
        elem, unknown = resource.NewBoolProperty(false), true
    case plugin.UnknownNumberValue:
        elem, unknown = resource.NewNumberProperty(0), true
    case plugin.UnknownStringValue:
        elem, unknown = resource.NewStringProperty(""), true
    case plugin.UnknownArrayValue:
        elem, unknown = resource.NewArrayProperty([]resource.PropertyValue{}), true
    case plugin.UnknownAssetValue:
        elem, unknown = resource.NewAssetProperty(&resource.Asset{}), true
    case plugin.UnknownArchiveValue:
        elem, unknown = resource.NewArchiveProperty(&resource.Archive{}), true
    case plugin.UnknownObjectValue:
        elem, unknown = resource.NewObjectProperty(make(resource.PropertyMap)), true
    }
    if unknown {
        comp := resource.Computed{Element: elem}
        return resource.NewComputedProperty(comp), true
    }
    return resource.PropertyValue{}, false
}


// Copied from the `plugin` module (modified)
// marshalUnknownProperty marshals an unknown property in a way that lets us recover its type on the other end.
func marshalUnknownProperty(elem resource.PropertyValue) string {
    // Normal cases, these get sentinels.
    if elem.IsBool() {
        return plugin.UnknownBoolValue
    } else if elem.IsNumber() {
        return plugin.UnknownNumberValue
    } else if elem.IsString() {
        return plugin.UnknownStringValue
    } else if elem.IsArray() {
        return plugin.UnknownArrayValue
    } else if elem.IsAsset() {
        return plugin.UnknownAssetValue
    } else if elem.IsArchive() {
        return plugin.UnknownArchiveValue
    } else if elem.IsObject() {
        return plugin.UnknownObjectValue
    }

    // If for some reason we end up with a recursive computed/output, just keep digging.
    if elem.IsComputed() {
        return marshalUnknownProperty(elem.Input().Element)
    } else if elem.IsOutput() {
        return marshalUnknownProperty(elem.OutputValue().Element)
    }

    // Finally, if a null, we can guess its value!  (the one and only...)
    return UnknownNullValue
}


func JSONToPropertyMap(data []byte) (resource.PropertyMap, error) {

    raw := make(map[string]interface{})

    if err := json.Unmarshal(data, &raw); err != nil {
        return nil, fmt.Errorf("error unmarshalling data: %v", err)
    }

    replv := func(value interface{}) (resource.PropertyValue, bool) {
        switch i := value.(type) {
        case map[string]interface{}:
            one := false
            for key, _ := range i {
                one = true
                if key != UnknownKey {
                    return resource.NewNullProperty(), false
                }
            }
            if one {
                val := i[UnknownKey].(string)
                property, _ := unmarshalUnknownPropertyValue(val)
                return property, true
            }
        }
        return resource.NewNullProperty(), false
    }

    return resource.NewPropertyMapFromMapRepl(raw, nil, replv), nil
}


func PropertyMapToJSON(data resource.PropertyMap) ([]byte, error) {

    var mapper func(resource.PropertyValue) (interface{}, bool)
    mapper = func(value resource.PropertyValue) (interface{}, bool) {
        switch v := value.V.(type) {
        case resource.PropertyMap:
            return v.MapRepl(nil, mapper), true
        case resource.PropertyValue:
            return mapper(v)
        case []resource.PropertyValue:
            var out []interface{}
            for _, item := range v {
                if obj, add := mapper(item); add {
                    out = append(out, obj)
                }
            }
            return out, true
        case resource.Computed:
            out := make(map[string]interface{})
            out[UnknownKey] = marshalUnknownProperty(v.Element)
            return out, true
        }
        return value.V, true
    }

    simpleMap := data.MapRepl(nil, mapper)
    out, err := json.Marshal(simpleMap)
    if err != nil {
        return nil, fmt.Errorf("error marshalling property map: %v", err)
    }

    return out, nil
}
