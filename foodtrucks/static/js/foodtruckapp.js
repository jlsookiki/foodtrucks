
    var IMAGE_LOC = '/static/images';

    var App = {};

    App.foodTruck = Backbone.GoogleMaps.Location.extend({
        idAttribute: 'owner'
    });

    App.foodTruckCollection = Backbone.GoogleMaps.LocationCollection.extend({
        model: App.foodTruck,
        url: '/trucks/area'


    });

    App.InfoWindow = Backbone.GoogleMaps.InfoWindow.extend({
        template: '#markerViewTemplate'
    });

    App.MarkerView = Backbone.GoogleMaps.MarkerView.extend({
        infoWindow: App.InfoWindow
    });

    App.FoodTruckMarker = App.MarkerView.extend({
        overlayOptions:{
            draggable: false,
            icon: IMAGE_LOC + '/foodtruck.png'
        }
    });

    App.PushCartMarker = App.MarkerView.extend({
        overlayOptions:{
            draggable: false,
            icon: IMAGE_LOC + '/foodtruck.png'
        }
    });

    App.MarkerCollectionView = Backbone.GoogleMaps.MarkerCollectionView.extend({
        markerView: App.MarkerView,

        addChild: function(model){
            this.markerView = model.get('type') === 'Truck' ?
                App.FoodTruckMarker :
                App.PushCartMarker;

            model.markerView = Backbone.GoogleMaps.MarkerCollectionView.prototype.addChild.apply(this, arguments);
        }
    });

    App.ItemView = Backbone.View.extend({
        template: '#listItemView',
        tagName: 'li',

        initialize: function(params) {
            this.owner = params.owner;
            this.collection = params.collection;
            _.bindAll(this, 'render', 'selectItem', 'deselectItem', 'click');
           // this.model.on("remove", this.close, this);
        },
        render: function() {
            var html = _.template($(this.template).html());
            this.$el.html(html({owner: this.owner}));
            return this;
        },
        close: function() {
            this.$el.remove();
        },
        selectItem: function() {
        //    this.model.select();
        },
        deselectItem: function() {
         //   this.model.deselect();
        },
        click: function(){
            console.log('changing');
        }

    });

    App.ListView = Backbone.View.extend({

        initialize: function() {
            _.bindAll(this, "refresh", "addChild");
            //this.collection.on("reset", this.refresh, this);
            //this.collection.on("add", this.addChild, this);
            this.$el.appendTo('body');
        },
        render: function() {
            var listview = this;
            _.each(this.collection, function(item, owner){
                listview.addChild(owner, item);
            });
        },
        addChild: function(owner, childModel) {
            var childView = new App.ItemView({ owner: owner, collection: childModel });
            childView.render().$el.appendTo('#ownerListing');
        },
        refresh: function() {
            this.$el.empty();
            this.render();
        }
    });


    App.init = function() {
        this.createMap();

        this.places = new this.foodTruckCollection();

        this.markers = new this.MarkerCollectionView({
            collection: this.places,
            map: this.map
        });
        var trucks = this.places;
        google.maps.event.addListenerOnce(this.map, 'idle', function(){
            console.log('bounds');
            console.log(this.getBounds());
            var bounds = this.getBounds();

            trucks.fetch({
                data: $.param({bound1: {x: bounds.Ca.j, y: bounds.Ca.k}, bound2: {x: bounds.va.j, y: bounds.va.k}}),
                success: function(places){
                    var owners = places.groupBy(function(place) { return place.get('owner')});
                    console.log('owners');
                    console.log(owners);
                    var listView = new App.ListView({
                        collection: owners
                    });
                    listView.render();

                    $('.foodTruckBox').on('change', function(){
                        var truckOwner = this.id;
                        var trucks = places.where({owner: truckOwner});
                        _.each(trucks, function(truck) { truck.toggleMarker()});
                    });
                }
            });

        });


        //Handle checking/unchecking off all textboxes
        $('#allFoodTrucks').on('change', function(){
            var checked = this.checked;
            _.each($('.foodTruckBox'), function(checkbox){
                if (checkbox.checked != checked){
                    checkbox.checked = checked;
                    $(checkbox).trigger('change');
                }
            })
        });
    }

    App.createMap = function(){
        var mapOptions = {
            //Set the center to roughly the center of San Francisco
            center: new google.maps.LatLng(37.777037, -122.418031),
            zoom: 14,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        }

        this.map = new google.maps.Map($('#map_canvas')[0], mapOptions);
    };
