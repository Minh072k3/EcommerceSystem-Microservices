Chúng ta sẽ xây dựng một ứng dụng Android quản lý điện thoại và hãng sản xuất sử dụng SQLite. Dưới đây là cấu trúc thư mục và hướng dẫn từng bước.
## Cấu trúc thư mục dự án (theo mô hình MVC)
```
app/
├── src/
│   ├── main/
│   │   ├── java/com/example/phone_manager/
│   │   │   ├── adapter/          # Các Adapter cho RecyclerView
│   │   │   │   ├── ManufacturerAdapter.java
│   │   │   │   └── PhoneAdapter.java
│   │   │   ├── database/          # Xử lý database
│   │   │   │   ├── DatabaseHelper.java
│   │   │   │   ├── ManufacturerDao.java
│   │   │   │   └── PhoneDao.java
│   │   │   ├── model/             # Model
│   │   │   │   ├── Manufacturer.java
│   │   │   │   └── Phone.java
│   │   │   ├── ui/                # Các Activity
│   │   │   │   ├── MainActivity.java
│   │   │   │   ├── ManufacturerActivity.java
│   │   │   │   ├── PhoneActivity.java
│   │   │   │   ├── PhonesByManufacturerActivity.java
│   │   │   │   └── LargeScreenPhonesActivity.java
│   │   │   └── utils/             # Các tiện ích (nếu có)
│   │   ├── res/
│   │   │   ├── layout/
│   │   │   │   ├── activity_main.xml
│   │   │   │   ├── activity_manufacturer.xml
│   │   │   │   ├── activity_phone.xml
│   │   │   │   ├── activity_phones_by_manufacturer.xml
│   │   │   │   ├── activity_large_screen.xml
│   │   │   │   ├── item_manufacturer.xml
│   │   │   │   └── item_phone.xml
│   │   │   ├── layout-land/       # Layout cho chế độ ngang (tùy chọn)
│   │   │   └── ...
│   │   └── AndroidManifest.xml
│   └── test/
└── build.gradle
```
## Hướng dẫn code từng bước
### 1. Tạo model
#### Manufacturer.java
```java
package com.example.phone_manager.model;
public class Manufacturer {
    private int id;
    private String name;
    private String description;
    // Constructor, getters, setters
    public Manufacturer() {}
    public Manufacturer(int id, String name, String description) {
        this.id = id;
        this.name = name;
        this.description = description;
    }
    // Getters and setters
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    @Override
    public String toString() {
        return name;
    }
}
```
#### Phone.java
```java
package com.example.phone_manager.model;
public class Phone {
    private int id;
    private String name;
    private int manufacturerId;
    private double screenSize;
    private int rating;
    // Constructor, getters, setters
    public Phone() {}
    public Phone(int id, String name, int manufacturerId, double screenSize, int rating) {
        this.id = id;
        this.name = name;
        this.manufacturerId = manufacturerId;
        this.screenSize = screenSize;
        this.rating = rating;
    }
    // Getters and setters
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public int getManufacturerId() { return manufacturerId; }
    public void setManufacturerId(int manufacturerId) { this.manufacturerId = manufacturerId; }
    public double getScreenSize() { return screenSize; }
    public void setScreenSize(double screenSize) { this.screenSize = screenSize; }
    public int getRating() { return rating; }
    public void setRating(int rating) { this.rating = rating; }
}
```
### 2. Tạo DatabaseHelper
#### DatabaseHelper.java
```java
package com.example.phone_manager.database;
import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
public class DatabaseHelper extends SQLiteOpenHelper {
    private static final String DATABASE_NAME = "PhoneManager.db";
    private static final int DATABASE_VERSION = 1;
    // Bảng Manufacturer
    public static final String TABLE_MANUFACTURER = "manufacturer";
    public static final String COLUMN_MANUFACTURER_ID = "id";
    public static final String COLUMN_MANUFACTURER_NAME = "name";
    public static final String COLUMN_MANUFACTURER_DESCRIPTION = "description";
    // Bảng Phone
    public static final String TABLE_PHONE = "phone";
    public static final String COLUMN_PHONE_ID = "id";
    public static final String COLUMN_PHONE_NAME = "name";
    public static final String COLUMN_PHONE_MANUFACTURER_ID = "manufacturer_id";
    public static final String COLUMN_PHONE_SCREEN_SIZE = "screen_size";
    public static final String COLUMN_PHONE_RATING = "rating";
    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }
    @Override
    public void onCreate(SQLiteDatabase db) {
        // Tạo bảng Manufacturer
        String createManufacturerTable = "CREATE TABLE " + TABLE_MANUFACTURER + "("
                + COLUMN_MANUFACTURER_ID + " INTEGER PRIMARY KEY AUTOINCREMENT,"
                + COLUMN_MANUFACTURER_NAME + " TEXT,"
                + COLUMN_MANUFACTURER_DESCRIPTION + " TEXT)";
        db.execSQL(createManufacturerTable);
        // Tạo bảng Phone
        String createPhoneTable = "CREATE TABLE " + TABLE_PHONE + "("
                + COLUMN_PHONE_ID + " INTEGER PRIMARY KEY AUTOINCREMENT,"
                + COLUMN_PHONE_NAME + " TEXT,"
                + COLUMN_PHONE_MANUFACTURER_ID + " INTEGER,"
                + COLUMN_PHONE_SCREEN_SIZE + " REAL,"
                + COLUMN_PHONE_RATING + " INTEGER,"
                + "FOREIGN KEY(" + COLUMN_PHONE_MANUFACTURER_ID + ") REFERENCES "
                + TABLE_MANUFACTURER + "(" + COLUMN_MANUFACTURER_ID + "))";
        db.execSQL(createPhoneTable);
    }
    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_PHONE);
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_MANUFACTURER);
        onCreate(db);
    }
}
```
### 3. Tạo Data Access Object (DAO)
#### ManufacturerDao.java
```java
package com.example.phone_manager.database;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import com.example.phone_manager.model.Manufacturer;
import java.util.ArrayList;
import java.util.List;
public class ManufacturerDao {
    private DatabaseHelper dbHelper;
    public ManufacturerDao(Context context) {
        dbHelper = new DatabaseHelper(context);
    }
    // Thêm hãng sản xuất
    public long addManufacturer(Manufacturer manufacturer) {
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(DatabaseHelper.COLUMN_MANUFACTURER_NAME, manufacturer.getName());
        values.put(DatabaseHelper.COLUMN_MANUFACTURER_DESCRIPTION, manufacturer.getDescription());
        long id = db.insert(DatabaseHelper.TABLE_MANUFACTURER, null, values);
        db.close();
        return id;
    }
    // Lấy tất cả hãng sản xuất
    public List<Manufacturer> getAllManufacturers() {
        List<Manufacturer> manufacturers = new ArrayList<>();
        SQLiteDatabase db = dbHelper.getReadableDatabase();
        Cursor cursor = db.query(DatabaseHelper.TABLE_MANUFACTURER,
                new String[]{DatabaseHelper.COLUMN_MANUFACTURER_ID,
                        DatabaseHelper.COLUMN_MANUFACTURER_NAME,
                        DatabaseHelper.COLUMN_MANUFACTURER_DESCRIPTION},
                null, null, null, null, null);
        if (cursor.moveToFirst()) {
            do {
                Manufacturer manufacturer = new Manufacturer();
                manufacturer.setId(cursor.getInt(cursor.getColumnIndex(DatabaseHelper.COLUMN_MANUFACTURER_ID)));
                manufacturer.setName(cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_MANUFACTURER_NAME)));
                manufacturer.setDescription(cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_MANUFACTURER_DESCRIPTION)));
                manufacturers.add(manufacturer);
            } while (cursor.moveToNext());
        }
        cursor.close();
        db.close();
        return manufacturers;
    }
    // Cập nhật hãng sản xuất
    public int updateManufacturer(Manufacturer manufacturer) {
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(DatabaseHelper.COLUMN_MANUFACTURER_NAME, manufacturer.getName());
        values.put(DatabaseHelper.COLUMN_MANUFACTURER_DESCRIPTION, manufacturer.getDescription());
        return db.update(DatabaseHelper.TABLE_MANUFACTURER, values,
                DatabaseHelper.COLUMN_MANUFACTURER_ID + " = ?",
                new String[]{String.valueOf(manufacturer.getId())});
    }
    // Xóa hãng sản xuất
    public void deleteManufacturer(int manufacturerId) {
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        db.delete(DatabaseHelper.TABLE_MANUFACTURER,
                DatabaseHelper.COLUMN_MANUFACTURER_ID + " = ?",
                new String[]{String.valueOf(manufacturerId)});
        db.close();
    }
}
```
#### PhoneDao.java
```java
package com.example.phone_manager.database;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import com.example.phone_manager.model.Phone;
import java.util.ArrayList;
import java.util.List;
public class PhoneDao {
    private DatabaseHelper dbHelper;
    public PhoneDao(Context context) {
        dbHelper = new DatabaseHelper(context);
    }
    // Thêm điện thoại
    public long addPhone(Phone phone) {
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(DatabaseHelper.COLUMN_PHONE_NAME, phone.getName());
        values.put(DatabaseHelper.COLUMN_PHONE_MANUFACTURER_ID, phone.getManufacturerId());
        values.put(DatabaseHelper.COLUMN_PHONE_SCREEN_SIZE, phone.getScreenSize());
        values.put(DatabaseHelper.COLUMN_PHONE_RATING, phone.getRating());
        long id = db.insert(DatabaseHelper.TABLE_PHONE, null, values);
        db.close();
        return id;
    }
    // Lấy tất cả điện thoại
    public List<Phone> getAllPhones() {
        List<Phone> phones = new ArrayList<>();
        SQLiteDatabase db = dbHelper.getReadableDatabase();
        Cursor cursor = db.query(DatabaseHelper.TABLE_PHONE,
                new String[]{DatabaseHelper.COLUMN_PHONE_ID,
                        DatabaseHelper.COLUMN_PHONE_NAME,
                        DatabaseHelper.COLUMN_PHONE_MANUFACTURER_ID,
                        DatabaseHelper.COLUMN_PHONE_SCREEN_SIZE,
                        DatabaseHelper.COLUMN_PHONE_RATING},
                null, null, null, null, null);
        if (cursor.moveToFirst()) {
            do {
                Phone phone = new Phone();
                phone.setId(cursor.getInt(cursor.getColumnIndex(DatabaseHelper.COLUMN_PHONE_ID)));
                phone.setName(cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_PHONE_NAME)));
                phone.setManufacturerId(cursor.getInt(cursor.getColumnIndex(DatabaseHelper.COLUMN_PHONE_MANUFACTURER_ID)));
                phone.setScreenSize(cursor.getDouble(cursor.getColumnIndex(DatabaseHelper.COLUMN_PHONE_SCREEN_SIZE)));
                phone.setRating(cursor.getInt(cursor.getColumnIndex(DatabaseHelper.COLUMN_PHONE_RATING)));
                phones.add(phone);
            } while (cursor.moveToNext());
        }
        cursor.close();
        db.close();
        return phones;
    }
    // Lấy điện thoại theo hãng sản xuất
    public List<Phone> getPhonesByManufacturer(int manufacturerId) {
        List<Phone> phones = new ArrayList<>();
        SQLiteDatabase db = dbHelper.getReadableDatabase();
        Cursor cursor = db.query(DatabaseHelper.TABLE_PHONE,
                new String[]{DatabaseHelper.COLUMN_PHONE_ID,
                        DatabaseHelper.COLUMN_PHONE_NAME,
                        DatabaseHelper.COLUMN_PHONE_MANUFACTURER_ID,
                        DatabaseHelper.COLUMN_PHONE_SCREEN_SIZE,
                        DatabaseHelper.COLUMN_PHONE_RATING},
                DatabaseHelper.COLUMN_PHONE_MANUFACTURER_ID + " = ?",
                new String[]{String.valueOf(manufacturerId)}, null, null, null);
        if (cursor.moveToFirst()) {
            do {
                Phone phone = new Phone();
                phone.setId(cursor.getInt(cursor.getColumnIndex(DatabaseHelper.COLUMN_PHONE_ID)));
                phone.setName(cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_PHONE_NAME)));
                phone.setManufacturerId(cursor.getInt(cursor.getColumnIndex(DatabaseHelper.COLUMN_PHONE_MANUFACTURER_ID)));
                phone.setScreenSize(cursor.getDouble(cursor.getColumnIndex(DatabaseHelper.COLUMN_PHONE_SCREEN_SIZE)));
                phone.setRating(cursor.getInt(cursor.getColumnIndex(DatabaseHelper.COLUMN_PHONE_RATING)));
                phones.add(phone);
            } while (cursor.moveToNext());
        }
        cursor.close();
        db.close();
        return phones;
    }
    // Lấy điện thoại có màn hình > 6 inch
    public List<Phone> getLargeScreenPhones() {
        List<Phone> phones = new ArrayList<>();
        SQLiteDatabase db = dbHelper.getReadableDatabase();
        String query = "SELECT * FROM " + DatabaseHelper.TABLE_PHONE +
                " WHERE " + DatabaseHelper.COLUMN_PHONE_SCREEN_SIZE + " > 6.0";
        Cursor cursor = db.rawQuery(query, null);
        if (cursor.moveToFirst()) {
            do {
                Phone phone = new Phone();
                phone.setId(cursor.getInt(cursor.getColumnIndex(DatabaseHelper.COLUMN_PHONE_ID)));
                phone.setName(cursor.getString(cursor.getColumnIndex(DatabaseHelper.COLUMN_PHONE_NAME)));
                phone.setManufacturerId(cursor.getInt(cursor.getColumnIndex(DatabaseHelper.COLUMN_PHONE_MANUFACTURER_ID)));
                phone.setScreenSize(cursor.getDouble(cursor.getColumnIndex(DatabaseHelper.COLUMN_PHONE_SCREEN_SIZE)));
                phone.setRating(cursor.getInt(cursor.getColumnIndex(DatabaseHelper.COLUMN_PHONE_RATING)));
                phones.add(phone);
            } while (cursor.moveToNext());
        }
        cursor.close();
        db.close();
        return phones;
    }
    // Cập nhật điện thoại
    public int updatePhone(Phone phone) {
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(DatabaseHelper.COLUMN_PHONE_NAME, phone.getName());
        values.put(DatabaseHelper.COLUMN_PHONE_MANUFACTURER_ID, phone.getManufacturerId());
        values.put(DatabaseHelper.COLUMN_PHONE_SCREEN_SIZE, phone.getScreenSize());
        values.put(DatabaseHelper.COLUMN_PHONE_RATING, phone.getRating());
        return db.update(DatabaseHelper.TABLE_PHONE, values,
                DatabaseHelper.COLUMN_PHONE_ID + " = ?",
                new String[]{String.valueOf(phone.getId())});
    }
    // Xóa điện thoại
    public void deletePhone(int phoneId) {
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        db.delete(DatabaseHelper.TABLE_PHONE,
                DatabaseHelper.COLUMN_PHONE_ID + " = ?",
                new String[]{String.valueOf(phoneId)});
        db.close();
    }
}
```
### 4. Tạo Adapter
#### ManufacturerAdapter.java
```java
package com.example.phone_manager.adapter;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.example.phone_manager.R;
import com.example.phone_manager.model.Manufacturer;
import java.util.List;
public class ManufacturerAdapter extends RecyclerView.Adapter<ManufacturerAdapter.ViewHolder> {
    private List<Manufacturer> manufacturers;
    public ManufacturerAdapter(List<Manufacturer> manufacturers) {
        this.manufacturers = manufacturers;
    }
    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_manufacturer, parent, false);
        return new ViewHolder(view);
    }
    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Manufacturer manufacturer = manufacturers.get(position);
        holder.tvName.setText(manufacturer.getName());
        holder.tvDescription.setText(manufacturer.getDescription());
    }
    @Override
    public int getItemCount() {
        return manufacturers.size();
    }
    public static class ViewHolder extends RecyclerView.ViewHolder {
        public TextView tvName, tvDescription;
        public ViewHolder(View itemView) {
            super(itemView);
            tvName = itemView.findViewById(R.id.tvManufacturerName);
            tvDescription = itemView.findViewById(R.id.tvDescription);
        }
    }
}
```
#### PhoneAdapter.java
```java
package com.example.phone_manager.adapter;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.example.phone_manager.R;
import com.example.phone_manager.model.Phone;
import java.util.List;
public class PhoneAdapter extends RecyclerView.Adapter<PhoneAdapter.ViewHolder> {
    private List<Phone> phones;
    private OnItemClickListener listener;
    public interface OnItemClickListener {
        void onItemClick(Phone phone);
    }
    public PhoneAdapter(List<Phone> phones, OnItemClickListener listener) {
        this.phones = phones;
        this.listener = listener;
    }
    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_phone, parent, false);
        return new ViewHolder(view);
    }
    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Phone phone = phones.get(position);
        holder.tvName.setText(phone.getName());
        holder.tvScreenSize.setText(String.format("%.1f''", phone.getScreenSize()));
        holder.tvRating.setText(String.valueOf(phone.getRating()));
        holder.itemView.setOnClickListener(v -> {
            if (listener != null) {
                listener.onItemClick(phone);
            }
        });
    }
    @Override
    public int getItemCount() {
        return phones.size();
    }
    public static class ViewHolder extends RecyclerView.ViewHolder {
        public TextView tvName, tvScreenSize, tvRating;
        public ViewHolder(View itemView) {
            super(itemView);
            tvName = itemView.findViewById(R.id.tvPhoneName);
            tvScreenSize = itemView.findViewById(R.id.tvScreenSize);
            tvRating = itemView.findViewById(R.id.tvRating);
        }
    }
}
```
### 5. Tạo Activity
#### MainActivity.java
```java
package com.example.phone_manager.ui;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;
import com.example.phone_manager.R;
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Button btnManageManufacturers = findViewById(R.id.btnManageManufacturers);
        Button btnManagePhones = findViewById(R.id.btnManagePhones);
        Button btnPhonesByManufacturer = findViewById(R.id.btnPhonesByManufacturer);
        Button btnLargeScreenPhones = findViewById(R.id.btnLargeScreenPhones);
        btnManageManufacturers.setOnClickListener(v -> {
            startActivity(new Intent(MainActivity.this, ManufacturerActivity.class));
        });
        btnManagePhones.setOnClickListener(v -> {
            startActivity(new Intent(MainActivity.this, PhoneActivity.class));
        });
        btnPhonesByManufacturer.setOnClickListener(v -> {
            startActivity(new Intent(MainActivity.this, PhonesByManufacturerActivity.class));
        });
        btnLargeScreenPhones.setOnClickListener(v -> {
            startActivity(new Intent(MainActivity.this, LargeScreenPhonesActivity.class));
        });
    }
}
```
#### ManufacturerActivity.java
```java
package com.example.phone_manager.ui;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.example.phone_manager.R;
import com.example.phone_manager.adapter.ManufacturerAdapter;
import com.example.phone_manager.database.ManufacturerDao;
import com.example.phone_manager.model.Manufacturer;
import java.util.ArrayList;
import java.util.List;
public class ManufacturerActivity extends AppCompatActivity {
    private EditText etManufacturerId, etManufacturerName, etDescription;
    private Button btnAdd, btnUpdate, btnDelete;
    private RecyclerView rvManufacturers;
    private ManufacturerAdapter adapter;
    private List<Manufacturer> manufacturers = new ArrayList<>();
    private ManufacturerDao manufacturerDao;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_manufacturer);
        manufacturerDao = new ManufacturerDao(this);
        etManufacturerId = findViewById(R.id.etManufacturerId);
        etManufacturerName = findViewById(R.id.etManufacturerName);
        etDescription = findViewById(R.id.etDescription);
        btnAdd = findViewById(R.id.btnAddManufacturer);
        btnUpdate = findViewById(R.id.btnUpdateManufacturer);
        btnDelete = findViewById(R.id.btnDeleteManufacturer);
        rvManufacturers = findViewById(R.id.rvManufacturers);
        rvManufacturers.setLayoutManager(new LinearLayoutManager(this));
        adapter = new ManufacturerAdapter(manufacturers);
        rvManufacturers.setAdapter(adapter);
        loadManufacturers();
        btnAdd.setOnClickListener(v -> addManufacturer());
        btnUpdate.setOnClickListener(v -> updateManufacturer());
        btnDelete.setOnClickListener(v -> deleteManufacturer());
    }
    private void loadManufacturers() {
        manufacturers.clear();
        manufacturers.addAll(manufacturerDao.getAllManufacturers());
        adapter.notifyDataSetChanged();
    }
    private void addManufacturer() {
        String name = etManufacturerName.getText().toString().trim();
        String description = etDescription.getText().toString().trim();
        if (name.isEmpty()) {
            etManufacturerName.setError("Name is required");
            return;
        }
        Manufacturer manufacturer = new Manufacturer();
        manufacturer.setName(name);
        manufacturer.setDescription(description);
        long id = manufacturerDao.addManufacturer(manufacturer);
        if (id != -1) {
            Toast.makeText(this, "Manufacturer added", Toast.LENGTH_SHORT).show();
            clearForm();
            loadManufacturers();
        } else {
            Toast.makeText(this, "Error adding manufacturer", Toast.LENGTH_SHORT).show();
        }
    }
    private void updateManufacturer() {
        String idStr = etManufacturerId.getText().toString().trim();
        if (idStr.isEmpty()) {
            Toast.makeText(this, "Select a manufacturer first", Toast.LENGTH_SHORT).show();
            return;
        }
        int id = Integer.parseInt(idStr);
        String name = etManufacturerName.getText().toString().trim();
        String description = etDescription.getText().toString().trim();
        if (name.isEmpty()) {
            etManufacturerName.setError("Name is required");
            return;
        }
        Manufacturer manufacturer = new Manufacturer(id, name, description);
        int count = manufacturerDao.updateManufacturer(manufacturer);
        if (count > 0) {
            Toast.makeText(this, "Manufacturer updated", Toast.LENGTH_SHORT).show();
            clearForm();
            loadManufacturers();
        } else {
            Toast.makeText(this, "Error updating manufacturer", Toast.LENGTH_SHORT).show();
        }
    }
    private void deleteManufacturer() {
        String idStr = etManufacturerId.getText().toString().trim();
        if (idStr.isEmpty()) {
            Toast.makeText(this, "Select a manufacturer first", Toast.LENGTH_SHORT).show();
            return;
        }
        int id = Integer.parseInt(idStr);
        manufacturerDao.deleteManufacturer(id);
        Toast.makeText(this, "Manufacturer deleted", Toast.LENGTH_SHORT).show();
        clearForm();
        loadManufacturers();
    }
    private void clearForm() {
        etManufacturerId.setText("");
        etManufacturerName.setText("");
        etDescription.setText("");
    }
}
```
#### PhoneActivity.java
```java
package com.example.phone_manager.ui;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.example.phone_manager.R;
import com.example.phone_manager.adapter.PhoneAdapter;
import com.example.phone_manager.database.ManufacturerDao;
import com.example.phone_manager.database.PhoneDao;
import com.example.phone_manager.model.Manufacturer;
import com.example.phone_manager.model.Phone;
import java.util.ArrayList;
import java.util.List;
public class PhoneActivity extends AppCompatActivity implements PhoneAdapter.OnItemClickListener {
    private EditText etPhoneId, etPhoneName, etScreenSize, etRating;
    private Spinner spinnerManufacturer;
    private Button btnAdd, btnUpdate, btnDelete;
    private RecyclerView rvPhones;
    private PhoneAdapter adapter;
    private List<Phone> phones = new ArrayList<>();
    private List<Manufacturer> manufacturers = new ArrayList<>();
    private PhoneDao phoneDao;
    private ManufacturerDao manufacturerDao;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_phone);
        phoneDao = new PhoneDao(this);
        manufacturerDao = new ManufacturerDao(this);
        etPhoneId = findViewById(R.id.etPhoneId);
        etPhoneName = findViewById(R.id.etPhoneName);
        spinnerManufacturer = findViewById(R.id.spinnerManufacturer);
        etScreenSize = findViewById(R.id.etScreenSize);
        etRating = findViewById(R.id.etRating);
        btnAdd = findViewById(R.id.btnAddPhone);
        btnUpdate = findViewById(R.id.btnUpdatePhone);
        btnDelete = findViewById(R.id.btnDeletePhone);
        rvPhones = findViewById(R.id.rvPhones);
        // Setup RecyclerView
        int spanCount = getResources().getConfiguration().orientation ==
                android.content.res.Configuration.ORIENTATION_LANDSCAPE ? 3 : 2;
        rvPhones.setLayoutManager(new GridLayoutManager(this, spanCount));
        adapter = new PhoneAdapter(phones, this);
        rvPhones.setAdapter(adapter);
        loadManufacturers();
        loadPhones();
        btnAdd.setOnClickListener(v -> addPhone());
        btnUpdate.setOnClickListener(v -> updatePhone());
        btnDelete.setOnClickListener(v -> deletePhone());
    }
    private void loadManufacturers() {
        manufacturers.clear();
        manufacturers.addAll(manufacturerDao.getAllManufacturers());
        ArrayAdapter<Manufacturer> spinnerAdapter = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_item, manufacturers);
        spinnerAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerManufacturer.setAdapter(spinnerAdapter);
    }
    private void loadPhones() {
        phones.clear();
        phones.addAll(phoneDao.getAllPhones());
        adapter.notifyDataSetChanged();
    }
    private void addPhone() {
        String name = etPhoneName.getText().toString().trim();
        Manufacturer selectedManufacturer = (Manufacturer) spinnerManufacturer.getSelectedItem();
        String screenSizeStr = etScreenSize.getText().toString().trim();
        String ratingStr = etRating.getText().toString().trim();
        if (name.isEmpty()) {
            etPhoneName.setError("Name is required");
            return;
        }
        if (selectedManufacturer == null) {
            Toast.makeText(this, "Select a manufacturer", Toast.LENGTH_SHORT).show();
            return;
        }
        if (screenSizeStr.isEmpty()) {
            etScreenSize.setError("Screen size is required");
            return;
        }
        if (ratingStr.isEmpty()) {
            etRating.setError("Rating is required");
            return;
        }
        double screenSize = Double.parseDouble(screenSizeStr);
        int rating = Integer.parseInt(ratingStr);
        Phone phone = new Phone();
        phone.setName(name);
        phone.setManufacturerId(selectedManufacturer.getId());
        phone.setScreenSize(screenSize);
        phone.setRating(rating);
        long id = phoneDao.addPhone(phone);
        if (id != -1) {
            Toast.makeText(this, "Phone added", Toast.LENGTH_SHORT).show();
            clearForm();
            loadPhones();
        } else {
            Toast.makeText(this, "Error adding phone", Toast.LENGTH_SHORT).show();
        }
    }
    private void updatePhone() {
        String idStr = etPhoneId.getText().toString().trim();
        if (idStr.isEmpty()) {
            Toast.makeText(this, "Select a phone first", Toast.LENGTH_SHORT).show();
            return;
        }
        int id = Integer.parseInt(idStr);
        String name = etPhoneName.getText().toString().trim();
        Manufacturer selectedManufacturer = (Manufacturer) spinnerManufacturer.getSelectedItem();
        String screenSizeStr = etScreenSize.getText().toString().trim();
        String ratingStr = etRating.getText().toString().trim();
        if (name.isEmpty()) {
            etPhoneName.setError("Name is required");
            return;
        }
        if (selectedManufacturer == null) {
            Toast.makeText(this, "Select a manufacturer", Toast.LENGTH_SHORT).show();
            return;
        }
        if (screenSizeStr.isEmpty()) {
            etScreenSize.setError("Screen size is required");
            return;
        }
        if (ratingStr.isEmpty()) {
            etRating.setError("Rating is required");
            return;
        }
        double screenSize = Double.parseDouble(screenSizeStr);
        int rating = Integer.parseInt(ratingStr);
        Phone phone = new Phone(id, name, selectedManufacturer.getId(), screenSize, rating);
        int count = phoneDao.updatePhone(phone);
        if (count > 0) {
            Toast.makeText(this, "Phone updated", Toast.LENGTH_SHORT).show();
            clearForm();
            loadPhones();
        } else {
            Toast.makeText(this, "Error updating phone", Toast.LENGTH_SHORT).show();
        }
    }
    private void deletePhone() {
        String idStr = etPhoneId.getText().toString().trim();
        if (idStr.isEmpty()) {
            Toast.makeText(this, "Select a phone first", Toast.LENGTH_SHORT).show();
            return;
        }
        int id = Integer.parseInt(idStr);
        phoneDao.deletePhone(id);
        Toast.makeText(this, "Phone deleted", Toast.LENGTH_SHORT).show();
        clearForm();
        loadPhones();
    }
    private void clearForm() {
        etPhoneId.setText("");
        etPhoneName.setText("");
        etScreenSize.setText("");
        etRating.setText("");
        if (manufacturers.size() > 0) {
            spinnerManufacturer.setSelection(0);
        }
    }
    @Override
    public void onItemClick(Phone phone) {
        etPhoneId.setText(String.valueOf(phone.getId()));
        etPhoneName.setText(phone.getName());
        etScreenSize.setText(String.valueOf(phone.getScreenSize()));
        etRating.setText(String.valueOf(phone.getRating()));
        // Select the manufacturer in spinner
        for (int i = 0; i < manufacturers.size(); i++) {
            if (manufacturers.get(i).getId() == phone.getManufacturerId()) {
                spinnerManufacturer.setSelection(i);
                break;
            }
        }
    }
}
```
#### PhonesByManufacturerActivity.java
```java
package com.example.phone_manager.ui;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.example.phone_manager.R;
import com.example.phone_manager.adapter.PhoneAdapter;
import com.example.phone_manager.database.ManufacturerDao;
import com.example.phone_manager.database.PhoneDao;
import com.example.phone_manager.model.Manufacturer;
import com.example.phone_manager.model.Phone;
import java.util.ArrayList;
import java.util.List;
public class PhonesByManufacturerActivity extends AppCompatActivity {
    private Spinner spinnerManufacturer;
    private RecyclerView rvPhones;
    private PhoneAdapter adapter;
    private List<Phone> phones = new ArrayList<>();
    private ManufacturerDao manufacturerDao;
    private PhoneDao phoneDao;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_phones_by_manufacturer);
        manufacturerDao = new ManufacturerDao(this);
        phoneDao = new PhoneDao(this);
        spinnerManufacturer = findViewById(R.id.spinnerManufacturerFilter);
        rvPhones = findViewById(R.id.rvPhonesByManufacturer);
        // Setup RecyclerView
        int spanCount = getResources().getConfiguration().orientation ==
                android.content.res.Configuration.ORIENTATION_LANDSCAPE ? 3 : 2;
        rvPhones.setLayoutManager(new GridLayoutManager(this, spanCount));
        adapter = new PhoneAdapter(phones, null); // No click listener needed
        rvPhones.setAdapter(adapter);
        loadManufacturers();
    }
    private void loadManufacturers() {
        List<Manufacturer> manufacturers = manufacturerDao.getAllManufacturers();
        ArrayAdapter<Manufacturer> spinnerAdapter = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_item, manufacturers);
        spinnerAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerManufacturer.setAdapter(spinnerAdapter);
        // Load phones when manufacturer selected
        spinnerManufacturer.setOnItemSelectedListener(new android.widget.AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(android.widget.AdapterView<?> parent, View view, int position, long id) {
                Manufacturer selected = (Manufacturer) parent.getSelectedItem();
                loadPhonesByManufacturer(selected.getId());
            }
            @Override
            public void onNothingSelected(android.widget.AdapterView<?> parent) {
            }
        });
        if (manufacturers.size() > 0) {
            loadPhonesByManufacturer(manufacturers.get(0).getId());
        }
    }
    private void loadPhonesByManufacturer(int manufacturerId) {
        phones.clear();
        phones.addAll(phoneDao.getPhonesByManufacturer(manufacturerId));
        adapter.notifyDataSetChanged();
    }
}
```
#### LargeScreenPhonesActivity.java
```java
package com.example.phone_manager.ui;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.example.phone_manager.R;
import com.example.phone_manager.adapter.PhoneAdapter;
import com.example.phone_manager.database.PhoneDao;
import com.example.phone_manager.model.Phone;
import java.util.ArrayList;
import java.util.List;
public class LargeScreenPhonesActivity extends AppCompatActivity {
    private RecyclerView rvLargeScreenPhones;
    private PhoneAdapter adapter;
    private List<Phone> phones = new ArrayList<>();
    private PhoneDao phoneDao;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_large_screen);
        phoneDao = new PhoneDao(this);
        rvLargeScreenPhones = findViewById(R.id.rvLargeScreenPhones);
        // Setup RecyclerView
        int spanCount = getResources().getConfiguration().orientation ==
                android.content.res.Configuration.ORIENTATION_LANDSCAPE ? 3 : 2;
        rvLargeScreenPhones.setLayoutManager(new GridLayoutManager(this, spanCount));
        adapter = new PhoneAdapter(phones, null); // No click listener needed
        rvLargeScreenPhones.setAdapter(adapter);
        loadLargeScreenPhones();
    }
    private void loadLargeScreenPhones() {
        phones.clear();
        phones.addAll(phoneDao.getLargeScreenPhones());
        adapter.notifyDataSetChanged();
    }
}
```
### 6. Layout XML files
#### item_manufacturer.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.cardview.widget.CardView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_margin="8dp">
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="16dp">
        <TextView
            android:id="@+id/tvManufacturerName"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:textStyle="bold"
            android:textSize="16sp"/>
        <TextView
            android:id="@+id/tvDescription"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="4dp"/>
    </LinearLayout>
</androidx.cardview.widget.CardView>
```
#### item_phone.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.cardview.widget.CardView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_margin="8dp">
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="16dp">
        <TextView
            android:id="@+id/tvPhoneName"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:textStyle="bold"
            android:textSize="16sp"/>
        <TextView
            android:id="@+id/tvScreenSize"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="4dp"/>
        <TextView
            android:id="@+id/tvRating"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="4dp"/>
    </LinearLayout>
</androidx.cardview.widget.CardView>
```
### 7. AndroidManifest.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.phone_manager">
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name=".ui.LargeScreenPhonesActivity"/>
        <activity android:name=".ui.PhonesByManufacturerActivity" />
        <activity android:name=".ui.PhoneActivity" />
        <activity android:name=".ui.ManufacturerActivity" />
        <activity android:name=".ui.MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```
## Giải thích
1. **Mô hình MVC**:
   - **Model**: Các lớp `Manufacturer` và `Phone` đại diện cho dữ liệu.
   - **View**: Các file layout XML.
   - **Controller**: Các Activity và DAO xử lý logic.
2. **SQLite Database**:
   - Sử dụng `SQLiteOpenHelper` để tạo và quản lý database.
   - Các DAO đóng gói các thao tác CRUD.
3. **RecyclerView**:
   - Hiển thị danh sách dữ liệu hiệu quả.
   - Adapter kết nối dữ liệu với View.
4. **Responsive Design**:
   - Sử dụng `GridLayoutManager` để thay đổi số cột theo hướng màn hình.
   - Layout weight cho các nút hành động.
   - `ScrollView` cho các form dài.
5. **Tương tác người dùng**:
   - Spinner để chọn hãng sản xuất.
   - RecyclerView với item click listener.
   - Form nhập liệu với validation.
